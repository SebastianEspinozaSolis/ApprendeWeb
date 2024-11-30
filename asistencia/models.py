from django.db import models
from usuarios.models import Alumno
from asignatura.models import Asignatura
# tabla asistencia
class Asistencia(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)  # Relación con el alumno
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)  # Relación con la asignatura
    fecha = models.DateField() 
    asistio = models.BooleanField(default=False)