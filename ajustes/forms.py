from django import forms
from .models import Ajustes

class AjustesForm(forms.ModelForm):
    class Meta:
        model = Ajustes
        exclude = ['usuario']
        widgets = {
            'tema_oscuro': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'idioma': forms.Select(attrs={'class': 'form-select'}),
            'notificaciones_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tamaño_fuente': forms.Select(attrs={'class': 'form-select'}),
        }
