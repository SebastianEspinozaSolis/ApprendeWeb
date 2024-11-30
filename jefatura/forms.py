from django import forms
from .models import Jefatura
from curso.models import Curso
from usuarios.models import Profesor
#formulario jefatura
class JefaturaForm(forms.ModelForm):
    curso = forms.ModelChoiceField(queryset=Curso.objects.all(), label='Curso')
    profesor = forms.ModelChoiceField(queryset=Profesor.objects.all(), label='Profesor')
    class Meta:
        model = Jefatura
        fields = ['curso','profesor']