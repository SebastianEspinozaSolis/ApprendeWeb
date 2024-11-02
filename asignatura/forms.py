from django import forms
from .models import Asignatura
from curso.models import Curso

class AsignaturaForm(forms.ModelForm):
    curso = forms.ModelChoiceField(queryset=Curso.objects.all(), label='Curso')

    class Meta:
        model = Asignatura
        fields = ['nombre', 'curso']