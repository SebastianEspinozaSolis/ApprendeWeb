from django.db import models
from django.contrib.auth.models import User

class Ajustes(models.Model):
    IDIOMAS = [
        ('es', 'Español'),
        ('en', 'English'),
    ]
    
    TAMAÑOS_FUENTE = [
        ('pequeño', 'Pequeño'),
        ('mediano', 'Mediano'),
        ('grande', 'Grande'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tema_oscuro = models.BooleanField(default=False)
    idioma = models.CharField(max_length=2, choices=IDIOMAS, default='es')
    notificaciones_email = models.BooleanField(default=True)
    tamaño_fuente = models.CharField(max_length=10, choices=TAMAÑOS_FUENTE, default='mediano')

    class Meta:
        verbose_name_plural = "Ajustes"
