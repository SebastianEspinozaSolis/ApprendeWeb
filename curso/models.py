from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Curso(models.Model):
    nombre = models.CharField(max_length=20)
    sala = models.CharField(
        max_length=2,
        validators=[
            RegexValidator(
                regex='^[0-9a-zA-Z]*$',
                message='Solo se permiten números y letras',
                code='invalid_sala'
            )
        ]
    )

    def __str__(self):
        return self.nombre

class Asignatura(models.Model):
    nombre = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='asignaturas')
    profesor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asignaturas')

    def __str__(self):
        return self.nombre + ' - ' + self.curso.nombre + ' - ' + self.profesor.username
    