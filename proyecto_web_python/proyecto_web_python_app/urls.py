from django.urls import path

from proyecto_web_python_app import views

# URLs de la aplicación
urlpatterns = [
    path('', views.inicio, name="Inicio"),
    path('donaciones', views.donaciones, name="Donaciones"),
    path('consultas', views.consultas, name="Consultas"),
    path('documentos', views.documentos, name="Documentos"),
]