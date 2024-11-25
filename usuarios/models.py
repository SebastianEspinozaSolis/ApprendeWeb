from django.db import models
from django.contrib.auth.models import User #Importamos el modelo User de la app auth
from curso.models import Curso
from datetime import date
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
from django.utils import timezone

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

def default_profile_image():
    return 'fotos_perfil/user.png'
    

class Perfil(models.Model):
    ROLES = (#Definimos una tupla con los roles que puede tener un usuario
        ('administrador','Administrador'),
        ('profesor','Profesor'),
        ('apoderado','Apoderado'),
        ('alumno','Alumno')
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE)#Relación uno a uno con la tabla User
    rol=models.CharField(max_length=20,choices=ROLES)#Campo para el rol del usuario
    foto = models.ImageField(
        upload_to='fotos_perfil',
        null=True,
        blank=True
    )
    nombre = models.CharField(max_length=100, null=True, blank=True)  # Nombre del usuario
    rut = models.CharField(
        max_length=12, 
        null=True, 
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{7,8}-[0-9Kk]$',
                message='Formato de RUT inválido. Debe ser como 12345678-9',
                code='invalid_rut'
            ),
            validar_rut
        ]
    )
    fecha_nacimiento = models.DateField(null=True, blank=True)  # Fecha de nacimiento
    sexo = models.CharField(max_length=1, choices=(('M', 'Masculino'), ('F', 'Femenino')), null=True, blank=True)  # Sexo
    segundo_rol = models.CharField(max_length=20, choices=ROLES, null=True, blank=True, default='')
    

    def __str__(self):
        return f"{self.user.username} - {self.rol}"
    def calcular_edad(self):
        if self.fecha_nacimiento is None:
            return "Fecha no disponible"
        
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad -= 1
        return edad
class Administrador(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=100, null=True, blank=True)  # Nombre del usuario
    # Puedes agregar campos específicos para el administrador aquí

class Apoderado(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, null=True, blank=True)  # Ejemplo de campo específico
    def __str__(self):
        return f"nombre: {self.perfil.nombre} - rut: {self.perfil.rut}"

class Alumno(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    curso=models.ForeignKey(Curso,on_delete=models.CASCADE)
    apoderado=models.ForeignKey(Apoderado,on_delete=models.CASCADE)

    def __str__(self):
        return f"nombre: {self.perfil.nombre} - rut: {self.perfil.rut}"

class Profesor(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100, null=True, blank=True)  # Ejemplo de campo específico
    def __str__(self):
        return f"nombre: {self.perfil.nombre} - rut: {self.perfil.rut} - especialidad: {self.especialidad}"

class Clase(models.Model):
    asignatura = models.CharField(max_length=100)
    hora = models.TimeField()
    sala = models.CharField(max_length=50)
    fecha = models.DateField()
    alumno = models.ForeignKey('Perfil', on_delete=models.CASCADE, related_name='clases')

    class Meta:
        ordering = ['fecha', 'hora']

class Evaluacion(models.Model):
    TIPOS = (
        ('prueba', 'Prueba'),
        ('trabajo', 'Trabajo'),
        ('proyecto', 'Proyecto'),
    )
    asignatura = models.CharField(max_length=100)
    fecha = models.DateField()
    tipo = models.CharField(max_length=20, choices=TIPOS)
    alumno = models.ForeignKey('Perfil', on_delete=models.CASCADE, related_name='evaluaciones')

    class Meta:
        ordering = ['fecha']

class Asignatura(models.Model):
    nombre = models.CharField(max_length=100)
    alumno = models.ForeignKey('Perfil', on_delete=models.CASCADE, related_name='asignaturas')
    promedio = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    asistencia = models.IntegerField(default=0)  # porcentaje de asistencia

    def calcular_estado(self):
        return 'Aprobado' if self.promedio >= 4.0 and self.asistencia >= 75 else 'En riesgo'

class Calificacion(models.Model):
    alumno = models.ForeignKey('Perfil', on_delete=models.CASCADE, related_name='calificaciones')
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=3, decimal_places=1)
    fecha = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['fecha']

    def __str__(self):
        return f"{self.alumno.nombre} - {self.evaluacion.asignatura} - {self.nota}"
