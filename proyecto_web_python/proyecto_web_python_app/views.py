from django.shortcuts import render, HttpResponse, redirect
from .forms import FormularioDonacion
import logging
from .utils import client, db
import pymongo
from tika import parser
from .models import Documento
import os.path
from django.core.files.storage import default_storage
from django.template.loader import render_to_string
import io 
from wsgiref.util import FileWrapper
from django.db import models

logging.basicConfig(level=logging.NOTSET)  # Here
# ----------------------------------------
# Definición de vistas
# ----------------------------------------


def inicio(request):
    return render(request, "proyecto_web_python_app/inicio.html")


def donaciones(request):

    formulario_donacion = FormularioDonacion()

    if request.method == "POST":

        formulario_donacion = FormularioDonacion(request.POST, request.FILES)

        if formulario_donacion.is_valid():

            codigo_donacion = request.POST.get("codigo_donacion")
            tipo_operacion = request.POST.get("tipo_operacion")
            documentos = request.FILES.getlist("documentos")

            logging.info(documentos)

            for value in documentos:

                logging.info(type(value.file))

                logging.info(value.file)

                fichero = models.FileField(io.BytesIO(value.file.getvalue()))

                logging.info(type(fichero))
                
                d = Documento(nombre = value.name, longitud = value.size, extension = os.path.splitext(value.name)[1], fichero = fichero)
                d.save()

                pdfBytes = value.file.getvalue()
                pdfFile = io.BytesIO(pdfBytes)

                logging.info(type(pdfFile))

                

                coleccion = db["documentos"]
                x = coleccion.insert_one({"nombre": d.nombre, "extension": d.extension, "longitud": d.longitud})

                #response = HttpResponse(FileWrapper(pdfFile), content_type='application/pdf')
                #return response





        return redirect("/donaciones?valido")

    return render(request, "proyecto_web_python_app/donaciones.html")


def consultas(request):
    return render(request, "proyecto_web_python_app/consultas.html")


def documentos(request):
    return render(request, "proyecto_web_python_app/documentos.html")
