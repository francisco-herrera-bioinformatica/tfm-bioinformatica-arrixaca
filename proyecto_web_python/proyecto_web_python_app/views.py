from django.shortcuts import render, redirect
import numpy
from .utils import db
from .models import Documento
import os
from django.core.files.storage import default_storage
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import re
import datetime
from django.http import FileResponse
import tabula
import pandas as pd

# ----------------------------------------
# Definición de vistas
# ----------------------------------------

# Vista asociada a la pantalla de inicio
def inicio(request):
    return render(request, "proyecto_web_python_app/inicio.html")

# ----------------------------------------
# Vista asociada a la pantalla de donaciones
def donaciones(request):
    
    # Obtener la autenticación del usuario
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credenciales.txt")
    drive = GoogleDrive(gauth)

    # Obtener los códigos de donación
    coleccion = db['donaciones']
    codigos_db = coleccion.find({}, {"_id": 0, "codigo_donacion": 1})
    codigos = []
    for codigo in codigos_db:
        codigos.append(codigo.get("codigo_donacion"))

    # Si la petición es POST, guardar la información
    if request.method == "POST":

        # Modelo con los campos del formulario
        codigo_donacion = request.POST.get("codigo_donacion")
        tipo_trasplante = request.POST.get("tipo_trasplante")
        tipo_operacion = request.POST.get("tipo_operacion")
        documentos = request.FILES.getlist("documentos")

        # Recorrer los documentos para su guardado
        for documento in documentos:

            # Almacenar localmente en disco duro para redundancia
            fs = FileSystemStorage()
            extension = os.path.splitext(documento.name)[1]
            nombre = os.path.splitext(documento.name)[0]
            nombre_formateado = re.sub('[^A-Za-z0-9]+', '', nombre)

            nombre_fichero = codigo_donacion + "-" + nombre_formateado + extension # Ejemplo: E005221100235-EstudiopreAloTPH509407.pdf
            filename = fs.save(tipo_trasplante + "/" + codigo_donacion + "/" + nombre_fichero, documento)
            uploaded_file_url = fs.url(filename)

            # Almacenar remotamente en Google Drive
            carpeta = drive.ListFile({'q': "title = 'TFM_Documentos' and trashed = false"}).GetList()[0]
            copia = drive.CreateFile({'title': nombre_fichero, 'parents': [{'id': carpeta['id']}]})
            copia.SetContentFile(uploaded_file_url[1:])
            copia.Upload()
            copia.InsertPermission({
                'type': 'anyone',
                'value': 'anyone',
                'role': 'reader'
            })

            # Guardar metadatos en MongoDB
            modelo = Documento(nombre = nombre_fichero, extension = extension, longitud = documento.size)
            coleccion = db['documentos']
            x = coleccion.insert_one({"codigo_donacion": codigo_donacion, "nombre": modelo.nombre, "extension": modelo.extension, "longitud": modelo.longitud, "fecha_subida": datetime.datetime.now().strftime('%d/%m/%Y'), "id_google": copia.get('id'), "enlace_google": copia['alternateLink'], "ruta_gestor": "../gestor_documentos_local/" + filename})        

            if modelo.extension == ".pdf":
                coleccion = db['datamining']
                lista = tabula.read_pdf("../gestor_documentos_local/" + filename, pages='all')
                
                for df in lista:
                    for row in df.iterrows():
                        array = row[1].array
                        array = array[~pd.isnull(array)]
                        cadena = str(array)
                        cadena = cadena[cadena.find('[')+1:cadena.find(']')]
                        if cadena != "en blanco" and any(char.isdigit() for char in cadena):
                            coleccion.insert_one({"codigo_donacion": codigo_donacion, "documento_asociado": x.inserted_id, "datos_obtenidos": cadena})

        # Si es nueva donación, guardar sus metadatos en MongoDB
        if tipo_operacion == "001":
            coleccion = db['donaciones']
            x = coleccion.insert_one({"codigo_donacion": codigo_donacion, "tipo_trasplante": tipo_trasplante, "documentos_asociados": len(documentos), "fecha_actualizacion": datetime.datetime.now().strftime('%d/%m/%Y')})

        # Si es donación ya existente, actualizar sus metadatos en MongoDB
        if tipo_operacion == "002":
            coleccion = db['donaciones']
            consulta = {"codigo_donacion": codigo_donacion}
            x = coleccion.find_one(consulta)
            nuevos_valores = {"$set": {"documentos_asociados": x.get("documentos_asociados") + len(documentos), "fecha_actualizacion": datetime.datetime.now().strftime('%d/%m/%Y')}}
            x = coleccion.update_one(consulta, nuevos_valores)

        return redirect("/donaciones?valido")

    return render(request, "proyecto_web_python_app/donaciones.html", {"codigos": codigos})

# ----------------------------------------
# Vista asociada a la pantalla de consultas
def consultas(request):

    if request.method == "POST":

        # Obtener los documentos asociados a la donación
        coleccion = db['documentos']
        consulta = {"codigo_donacion": request.POST.get("codigo_donacion")}
        print(consulta)
        documentos = coleccion.find(consulta)

        # Obtener los datos de los documentos
        coleccion = db['datamining']
        lista_documentos = []
        for documento in documentos:
            consulta = {"documento_asociado": documento.get("_id")}
            documento["datos"] = coleccion.find(consulta)
            lista_documentos.append(documento)

        return render(request, "proyecto_web_python_app/consultas.html", {"documentos": lista_documentos})

    return render(request, "proyecto_web_python_app/consultas.html")

# ----------------------------------------
# Vista asociada a la pantalla de documentos
def documentos(request):

    # Obtener la autenticación del usuario
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credenciales.txt")

    coleccion = db['documentos']
    documentos = coleccion.find()

    # Descarga del documento desde el gestor de documentos local
    if request.method == "POST":

        dict = request.POST
        ruta_gestor = list(dict.keys())[-1]

        extension = os.path.splitext(ruta_gestor)[1]

        if extension == ".pdf":
            return FileResponse(open(ruta_gestor, 'rb'), content_type='application/pdf')

        if extension == ".doc":
            return FileResponse(open(ruta_gestor, 'rb'), content_type='application/ms-word')

    return render(request, "proyecto_web_python_app/documentos.html", {"documentos": documentos})
