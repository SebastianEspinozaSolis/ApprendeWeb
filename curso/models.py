from django.db import models
from django.contrib.auth.models import User

class Curso(models.Model):
    nombre = models.CharField(max_length=20)
    sala = models.CharField(max_length=20)

    def __str__(self):
        return self.titulo