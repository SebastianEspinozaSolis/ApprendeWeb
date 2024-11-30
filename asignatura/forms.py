from django import forms
from .models import Asignatura
from curso.models import Curso
from usuarios.models import Profesor
# formulario para asignatura
class AsignaturaForm(forms.ModelForm):
    curso = forms.ModelChoiceField(queryset=Curso.objects.all(), label='Curso')
    profesor = forms.ModelChoiceField(queryset=Profesor.objects.all(), label='Profesor')
    class Meta:
        model = Asignatura
        fields = ['nombre', 'curso','profesor']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }