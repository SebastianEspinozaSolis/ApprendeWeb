from django import forms
from .models import Evaluacion
from asignatura.models import Asignatura

class EvaluacionForm(forms.ModelForm):
    asignatura = forms.ModelChoiceField(queryset=Asignatura.objects.all(), label='Asignatura')

    class Meta:
        model = Evaluacion
        fields = ['nombre','descripcion','fecha', 'asignatura']
        widgets = {'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'  # Esto habilita el selector de fecha
            }),}