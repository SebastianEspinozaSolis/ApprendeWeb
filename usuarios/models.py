from django.db import models
from django.contrib.auth.models import User #Importamos el modelo User de la app auth
from curso.models import Curso
from datetime import date
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
# Create your models here.

def validar_rut(value):
    # Limpia el RUT de puntos y guión
    rut = value.replace(".", "").replace("-", "")
    # Verifica el formato usando regex
    if not re.match(r'^[0-9]{7,8}[0-9Kk]$', rut):
        raise ValidationError('Formato de RUT inválido')
    # Obtiene el dígito verificador
    dv = rut[-1].upper()
    rut = rut[:-1]
    # Calcula el dígito verificador
    factor = 2
    suma = 0
    for digit in reversed(rut):
        suma += int(digit) * factor
        factor = factor + 1 if factor < 7 else 2
    dv_calculado = str(11 - (suma % 11))
    if dv_calculado == '11':
        dv_calculado = '0'
    elif dv_calculado == '10':
        dv_calculado = 'K'
    if dv != dv_calculado:
        raise ValidationError('RUT inválido')
def validate_chilean_phone_number(value):
    # Validar que el número empiece con +569 seguido de 8 dígitos
    pattern = r'^\+569\d{8}$'
    if not re.match(pattern, value):
        raise ValidationError('El número de teléfono debe comenzar con +569 y ser seguido de 8 dígitos.')
#tabla perfil
class Perfil(models.Model):
    ROLES = (#Definimos una tupla con los roles que puede tener un usuario
        ('administrador','Administrador'),
        ('profesor','Profesor'),
        ('apoderado','Apoderado'),
        ('alumno','Alumno')
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE)#Relación uno a uno con la tabla User
    rol=models.CharField(max_length=20,choices=ROLES)#Campo para el rol del usuario
    foto=models.ImageField(upload_to='fotos_perfil',null=True,blank=True)#Campo para la foto del usuario
    nombre = models.CharField(max_length=100, null=False, blank=False)  # Nombre del usuario
    rut = models.CharField(max_length=12,null=False,blank=False,validators=[RegexValidator(regex=r'^[0-9]{7,8}-[0-9Kk]$',message='Formato de RUT inválido. Debe ser como 12345678-9',code='invalid_rut'),validar_rut])
    fecha_nacimiento = models.DateField(null=True, blank=True)  # Fecha de nacimiento
    sexo = models.CharField(max_length=1, choices=(('M', 'Masculino'), ('F', 'Femenino')), null=False, blank=False)  # Sexo
    #cuando se escriba se escribira el nickname y rol, no el id
    def __str__(self):
        return f"{self.user.username} - {self.rol}"
    #calcula la edad en base a la fecha nacimiento
    def calcular_edad(self):
        if self.fecha_nacimiento is None:
            return "Fecha no disponible"
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad -= 1
        return edad
#tabla administrador
class Administrador(models.Model):
    #uso de datos de perfil
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    #datos propios
    cargo = models.CharField(max_length=100, null=False, blank=False)  
#tabla apoderado
class Apoderado(models.Model):
    #uso de datos de perfil
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    #datos propios
    telefono = models.CharField(
        max_length=13,  # +569 seguido de 8 dígitos
        # validador
        validators=[validate_chilean_phone_number],
        blank=False, 
        null=False
    )
    # en caso de escribir apoderado mostrara el nombre y rut
    def __str__(self):
        return f"nombre: {self.perfil.nombre} - rut: {self.perfil.rut}"
#tabla alumno
class Alumno(models.Model):
    #uso de datos de perfil
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    #datos propios
    curso=models.ForeignKey(Curso,on_delete=models.CASCADE)
    apoderado=models.ForeignKey(Apoderado,on_delete=models.CASCADE)
    # en caso de escribir alumno mostrara el nombre y rut
    def __str__(self):
        return f"{self.perfil.nombre} ({self.perfil.rut})"
#tabla profesor
class Profesor(models.Model):
    #uso de datos de perfil
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    #datos propios
    especialidad = models.CharField(max_length=100, null=False, blank=False) 
    # en caso de escribir alumno mostrara el nombre, rut y la especialidad
    def __str__(self):
        return f"nombre: {self.perfil.nombre} - rut: {self.perfil.rut} - especialidad: {self.especialidad}"