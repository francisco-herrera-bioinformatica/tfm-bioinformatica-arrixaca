from django.db import models

# Create your models here.
class Documento(models.Model):
    nombre = models.CharField(max_length=255)
    extension = models.CharField(max_length=20)
    longitud = models.CharField(max_length=50)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='documento'
        verbose_name_plural='documentos'

    def __str__(self):
        return self.nombre
