from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Reporte(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona el reporte con el perfil del usuario
    titulo = models.CharField(max_length=255, null=False, blank=False)  # Título del reporte
    descripcion = models.TextField()  # Descripción del reporte (bug o sugerencia)
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación automática del reporte
    tipo = models.CharField(
        max_length=20,
        choices=[('bug', 'Bug'), ('sugerencia', 'Sugerencia')],
        default='bug'  # Por defecto el tipo es 'bug'
    )