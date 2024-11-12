from django.db import models
from usuarios.models import Perfil, Alumno  # Importa el perfil y el modelo de alumno

class Aviso(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creador = models.ForeignKey(Perfil, on_delete=models.CASCADE)  # Quién envía el aviso (perfil del administrador/profesor)

    def __str__(self):
        return self.titulo

class AvisoAlumno(models.Model):
    aviso = models.ForeignKey(Aviso, on_delete=models.CASCADE, related_name='avisos_alumno')
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)  # Alumnos destinatarios del aviso

    def __str__(self):
        return f"{self.aviso.titulo} - {self.alumno.perfil.nombre} ({self.alumno.perfil.rut})"