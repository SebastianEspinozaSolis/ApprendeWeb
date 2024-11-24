from django import forms
from django.contrib.auth.models import User
from .models import Perfil, Apoderado,Administrador,Alumno,Profesor
from curso.models import Curso

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    password_confirmacion = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')
    
    # Campos para el perfil
    nombre = forms.CharField(max_length=100, required=True, label='Nombre')
    rut = forms.CharField(max_length=12, required=True, label='RUT')
    fecha_nacimiento = forms.DateField(required=True, label='Fecha de Nacimiento', widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    sexo = forms.ChoiceField(choices=[('M', 'Masculino'), ('F', 'Femenino')], required=True, label='Sexo')
    rol = forms.ChoiceField(choices=Perfil.ROLES, label='Rol')
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmacion']  # Campos del modelo User

    def clean_password_confirmacion(self):
        password = self.cleaned_data.get('password')
        password_confirmacion = self.cleaned_data.get('password_confirmacion')
        if password and password_confirmacion and password != password_confirmacion:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password_confirmacion
class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = ['cargo']
class ApoderadoForm(forms.ModelForm):
    class Meta:
        model = Apoderado
        fields = ['telefono']  # Solo el campo teléfono del apoderado
class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['especialidad'] 
class AlumnoForm(forms.ModelForm):
    apoderado = forms.ModelChoiceField(queryset=Apoderado.objects.all(), label='Apoderado')
    curso = forms.ModelChoiceField(queryset=Curso.objects.all(), label='Curso')
    class Meta:
        model = Alumno
        fields = ['apoderado','curso']

class EditarForm(forms.ModelForm):
    # Campos para el perfil
    nombre = forms.CharField(max_length=100, required=True, label='Nombre')
    rut = forms.CharField(max_length=12, required=True, label='RUT')
    fecha_nacimiento = forms.DateField(required=True, label='Fecha de Nacimiento', widget=forms.widgets.DateInput(attrs={'type': 'date', 'placeholder': 'dd-mm-aaaa'}))
    sexo = forms.ChoiceField(choices=[('M', 'Masculino'), ('F', 'Femenino')], required=True, label='Sexo')
    rol = forms.ChoiceField(choices=Perfil.ROLES, label='Rol')
    
    class Meta:
        model = Perfil
        fields = ['nombre','rut','fecha_nacimiento','sexo','rol']
class EditarFotoPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto']
        widgets = {'foto': forms.FileInput(attrs={'class': 'form-control'}),}
class EditarCorreoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
class CambiarContraseñaForm(forms.Form):
    password_actual = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    nueva_password = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    confirmar_password = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        nueva_password = cleaned_data.get('nueva_password')
        confirmar_password = cleaned_data.get('confirmar_password')

        if nueva_password != confirmar_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data
