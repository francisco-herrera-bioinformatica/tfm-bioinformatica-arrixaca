from django import forms

class FormularioDonacion(forms.Form):

    codigo_donacion = forms.CharField(label="Codigo", required=True)
    tipo_operacion = forms.CharField(label="Tipo", required=True)
    documentos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))