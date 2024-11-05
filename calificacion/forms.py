from django import forms
from .models import Calificacion
from evaluacion.models import Evaluacion
from usuarios.models import Alumno

class CalificacionForm(forms.ModelForm):
    alumno = forms.ModelChoiceField(queryset=Alumno.objects.all(), label='Alumno')
    evaluacion = forms.ModelChoiceField(queryset=Evaluacion.objects.all(), label='Evaluacion')
    class Meta:
        model = Calificacion
        fields = ['calificacion', 'alumno', 'evaluacion']
    
class EditarCalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['calificacion']