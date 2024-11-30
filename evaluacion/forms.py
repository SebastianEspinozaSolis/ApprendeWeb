from django import forms
from .models import Evaluacion
from asignatura.models import Asignatura
#formulario evaluacion
class EvaluacionForm(forms.ModelForm):
    asignatura = forms.ModelChoiceField(queryset=Asignatura.objects.all(), label='Asignatura')
    class Meta:
        model = Evaluacion
        fields = ['nombre','descripcion','fecha', 'asignatura']
        widgets = {'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'  # Esto habilita el selector de fecha
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,  # Controlar la altura del campo de texto
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',  # Asegurando que todos los campos tengan el mismo estilo
            }),
        }