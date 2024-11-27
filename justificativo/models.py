from django.db import models
from usuarios.models import Alumno

class Justificativo(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]

    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)  # Referencia al modelo Alumno en otra app
    fecha = models.DateField()  # Fecha de la inasistencia a justificar
    motivo = models.TextField()  # Motivo de la justificación
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')  # Estado del justificativo
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Justificativo de {self.alumno} - {self.fecha}"
