from django.shortcuts import render, HttpResponse

# ----------------------------------------
# Definición de vistas
# ----------------------------------------

def inicio(request):
    return render(request, "proyecto_web_python_app/inicio.html")

def donaciones(request):
    return render(request, "proyecto_web_python_app/donaciones.html")
  
def consultas(request):
    return render(request, "proyecto_web_python_app/consultas.html")

def documentos(request):
    return render(request, "proyecto_web_python_app/documentos.html")


