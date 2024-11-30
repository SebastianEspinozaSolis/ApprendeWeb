from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
# tabla de curso
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
    # en caso que se escriba curso mostrara el nombre
    def __str__(self):
        return self.nombre