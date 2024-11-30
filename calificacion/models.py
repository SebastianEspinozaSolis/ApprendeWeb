from django.db import models
from django.contrib.auth.models import User
from asignatura.models import Asignatura
from usuarios.models import Alumno  
from evaluacion.models import Evaluacion  
#tabla de calificacion
class Calificacion(models.Model):
    calificacion = models.DecimalField(max_digits=3, decimal_places=1)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE) 
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE) 
    # en caso de escribir calificacion se mostrara como alumno - asignatura - calificacion
    def __str__(self):
        return f"{self.alumno.perfil.nombre} - {self.evaluacion.asignatura.nombre} - {self.calificacion}"