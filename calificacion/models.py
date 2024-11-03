from django.db import models
from django.contrib.auth.models import User
from asignatura.models import Asignatura

class Calificacion(models.Model):
    calificacion = models.DecimalField(max_digits=3, decimal_places=1)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
        
    def __str__(self):
        return self.calificacion