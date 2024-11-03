from django.db import models
from django.contrib.auth.models import User #Importamos el modelo User de la app auth
# Create your models here.

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
    nombre = models.CharField(max_length=100, null=True, blank=True)  # Nombre del usuario
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True)  # RUT del usuario
    fecha_nacimiento = models.DateField(null=True, blank=True)  # Fecha de nacimiento
    sexo = models.CharField(max_length=1, choices=(('M', 'Masculino'), ('F', 'Femenino')), null=True, blank=True)  # Sexo
    segundo_rol = models.CharField(max_length=20, choices=ROLES, null=True, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} - {self.rol}"