from django import forms
from .models import Curso
# formulario curso
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre', 'sala']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'sala': forms.TextInput(attrs={'class': 'form-control'}),
        }