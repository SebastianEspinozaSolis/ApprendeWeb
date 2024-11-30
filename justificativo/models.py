from django.db import models
from usuarios.models import Alumno
# tabla justificativo
class Justificativo(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)  
    fecha = models.DateField() 
    motivo = models.TextField() 
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # en caso que se escriba justificativo se mostrara del alumno y fecha
    def __str__(self):
        return f"Justificativo de {self.alumno} - {self.fecha}"
