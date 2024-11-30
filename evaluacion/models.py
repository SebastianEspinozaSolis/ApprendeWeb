from django.db import models
from django.contrib.auth.models import User
from asignatura.models import Asignatura
# tabla evaluacion
class Evaluacion(models.Model):
    nombre = models.CharField(max_length=100) 
    descripcion = models.CharField(max_length=255, default='Sin descripción')
    fecha = models.DateField()
    asignatura = models.ForeignKey(Asignatura,on_delete=models.CASCADE)
    def __str__(self):
        return self.fecha