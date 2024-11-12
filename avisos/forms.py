from django import forms
from .models import Aviso, AvisoAlumno
from usuarios.models import Alumno  # Importa el modelo de alumnos

class AvisoForm(forms.ModelForm):
    class Meta:
        model = Aviso
        fields = ['titulo', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }

class AvisoAlumnoForm(forms.Form):
    alumnos = forms.ModelMultipleChoiceField(
        queryset=Alumno.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Selecciona los alumnos destinatarios"
    )
