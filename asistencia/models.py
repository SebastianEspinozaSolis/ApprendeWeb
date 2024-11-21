from django.db import models
from django.conf import settings
from usuarios.models import Alumno

class Asistencia(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='asistencias')
    asignatura = models.ForeignKey('asignatura.Asignatura', on_delete=models.CASCADE)
    fecha = models.DateField()
    asistio = models.BooleanField(default=False)
    justificacion = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ['alumno', 'asignatura', 'fecha']

    def __str__(self):
        return f"{self.alumno} - {self.asignatura} - {self.fecha}"