from django.shortcuts import render, HttpResponse

# ----------------------------------------
# Definición de vistas
# ----------------------------------------

def inicio(request):
    return HttpResponse("Inicio")

def donaciones(request):
    return HttpResponse("Donaciones")
  
def consultas(request):
    return HttpResponse("Consultas")

def documentos(request):
    return HttpResponse("Documentos")


