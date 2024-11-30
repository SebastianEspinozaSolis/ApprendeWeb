from django.db import models
from django.contrib.auth.models import User
from curso.models import Curso
from usuarios.models import Profesor
# tabla asignatura
class Asignatura(models.Model):
    nombre = models.CharField(max_length=20)
    curso = models.ForeignKey(Curso,on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre