from django import forms
from .models import Asistencia
from usuarios.models import Alumno
from asignatura.models import Asignatura

class AsistenciaForm(forms.ModelForm):
    alumno = forms.ModelChoiceField(queryset=Alumno.objects.all(), label='Alumno')
    asignatura = forms.ModelChoiceField(queryset=Asignatura.objects.all(), label='Asignatura')
    fecha = forms.DateField(label='Fecha de Asistencia', widget=forms.SelectDateWidget())
    asistio = forms.BooleanField(label='Asistió', required=False)

    class Meta:
        model = Asistencia
        fields = ['alumno', 'asignatura', 'fecha', 'asistio']
        widgets = {'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'  # Esto habilita el selector de fecha
            }),}
    
class EditarAsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['asistio']  # Solo editable el campo 'asistio'
