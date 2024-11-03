from django import forms
from .models import Calificacion
from asignatura.models import Asignatura

class CalificacionForm(forms.ModelForm):
    asignatura = forms.ModelChoiceField(queryset=Asignatura.objects.all(), label='Asignatura')
    class Meta:
        model = Calificacion
        fields = ['calificacion', 'asignatura']
        widgets = {
            'calificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'asignatura': forms.TextInput(attrs={'class': 'form-control'}),
        }