from django import forms
from .models import Aviso, AvisoAlumno
from usuarios.models import Alumno  # Importa el modelo de alumnos
# formulario de contenido
class AvisoForm(forms.ModelForm):
    class Meta:
        model = Aviso
        fields = ['titulo', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }
# formulario de alumnos que se enviara
class AvisoAlumnoForm(forms.Form):
    seleccionar_todos = forms.BooleanField(
        required=False,
        label='Seleccionar todos los alumnos del curso',
        initial=False
    )
    alumnos = forms.ModelMultipleChoiceField(
        queryset=Alumno.objects.none(),  # Esto se actualizará dinámicamente
        widget=forms.CheckboxSelectMultiple,
        label="Selecciona los alumnos destinatarios",
        required=False
    )
    # obtiene los alumnos del curso
    def __init__(self, *args, **kwargs):
        curso_id = kwargs.pop('curso_id', None)  # Recibimos el curso_id desde la vista
        super().__init__(*args, **kwargs)
        if curso_id:
            # Filtramos los alumnos por el curso especificado
            self.fields['alumnos'].queryset = Alumno.objects.filter(curso_id=curso_id)
