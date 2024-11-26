from django import forms
from django.contrib.auth.models import User
from .models import Perfil, Apoderado,Administrador,Alumno,Profesor
from curso.models import Curso

class RegistroForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre de usuario'}), label='Usuario')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su correo electrónico'}), label='Correo Electrónico')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}), label='Contraseña')
    password_confirmacion = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme su contraseña'}), label='Confirmar Contraseña')
    
    # Campos para el perfil
    nombre = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}), label='Nombre')
    rut = forms.CharField(max_length=12, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su RUT'}), label='RUT')
    fecha_nacimiento = forms.DateField(required=True, label='Fecha de Nacimiento', widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    sexo = forms.ChoiceField(choices=[('M', 'Masculino'), ('F', 'Femenino')], required=True, label='Sexo', widget=forms.Select(attrs={'class': 'form-control'}))
    rol = forms.ChoiceField(choices=Perfil.ROLES, label='Rol', widget=forms.Select(attrs={'class': 'form-control'}))
    foto = forms.ImageField(required=False, label='Foto de Perfil', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmacion', 'foto']  # Campos del modelo User

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

class UsuarioForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre de usuario'}), label='Usuario')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su correo electrónico'}), label='Correo Electrónico')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}), label='Contraseña')
    password_confirmacion = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme su contraseña'}), label='Confirmar Contraseña')
    
    # Campos para el perfil
    nombre = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}), label='Nombre')
    rut = forms.CharField(max_length=12, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su RUT'}), label='RUT')
    fecha_nacimiento = forms.DateField(required=True, label='Fecha de Nacimiento', widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    sexo = forms.ChoiceField(choices=[('M', 'Masculino'), ('F', 'Femenino')], required=True, label='Sexo', widget=forms.Select(attrs={'class': 'form-control'}))
    rol = forms.ChoiceField(choices=Perfil.ROLES, label='Rol', widget=forms.Select(attrs={'class': 'form-control'}))
    foto = forms.ImageField(required=False, label='Foto de Perfil', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmacion', 'foto']


class EditarForm(forms.ModelForm):
    # Campos para el perfil
    nombre = forms.CharField(max_length=100, required=True, label='Nombre')
    rut = forms.CharField(max_length=12, required=True, label='RUT')
    fecha_nacimiento = forms.DateField(required=True, label='Fecha de Nacimiento', widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    sexo = forms.ChoiceField(choices=[('M', 'Masculino'), ('F', 'Femenino')], required=True, label='Sexo')
    rol = forms.ChoiceField(choices=Perfil.ROLES, label='Rol')
    segundo_rol = forms.ChoiceField(
        choices=[('', 'Ninguno')] + list(Perfil.ROLES),  # Añadir 'Ninguno' a las opciones
        initial='',  # Establecer 'Ninguno' como valor predeterminado
        label='Rol Secundario'
    )
    foto = forms.ImageField(
        required=False, 
        label='Foto de Perfil',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Perfil
        fields = ['nombre', 'rut', 'fecha_nacimiento', 'sexo', 'rol', 'segundo_rol', 'foto']  

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nombre', 'rut', 'fecha_nacimiento', 'sexo', 'foto']  