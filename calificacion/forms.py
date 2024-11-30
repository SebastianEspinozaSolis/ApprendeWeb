from django import forms
from .models import Calificacion
from evaluacion.models import Evaluacion
from usuarios.models import Alumno
# formulario al crear calificaciones
class CalificacionForm(forms.ModelForm):
    alumno = forms.ModelChoiceField(queryset=Alumno.objects.all(), label='Alumno')
    evaluacion = forms.ModelChoiceField(queryset=Evaluacion.objects.all(), label='Evaluacion')
    class Meta:
        model = Calificacion
        fields = ['calificacion', 'alumno', 'evaluacion']
#formulario al editar una calificacion
class EditarCalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['calificacion']