from django.db import models
from django.contrib.auth.models import User
from curso.models import Curso
from usuarios.models import Profesor
# tabla jefatura
class Jefatura(models.Model):
    curso = models.OneToOneField(Curso,on_delete=models.CASCADE)
    profesor = models.OneToOneField(Profesor, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.curso.nombre} - Jefatura de {self.profesor.perfil.nombre}"
    