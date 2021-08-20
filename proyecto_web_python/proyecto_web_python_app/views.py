from django.shortcuts import render, HttpResponse, redirect
from .forms import FormularioDonacion
import logging
from .utils import client, db
import pymongo
from tika import parser

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
            documentos = request.FILES

            for documento in documentos:
                raw = parser.from_file(documento)
                print(raw['content'])

        return redirect("/donaciones?valido")

    return render(request, "proyecto_web_python_app/donaciones.html")


def consultas(request):
    return render(request, "proyecto_web_python_app/consultas.html")


def documentos(request):
    return render(request, "proyecto_web_python_app/documentos.html")
