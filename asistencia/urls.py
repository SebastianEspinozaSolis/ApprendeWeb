from django.urls import path
from . import views

app_name = 'asistencia'

urlpatterns = [
    path('crear/<int:asignatura_id>/', views.crear_asistencia, name='crear_asistencia'),  # Aquí pasamos asignatura_id
    path('editar/<int:pk>/', views.editar_asistencia, name='editar_asistencia'),
    path('fechas/<int:asignatura_id>/', views.lista_fechas_asistencia, name='lista_fechas_asistencia'),
     path('detalle_asistencia/<int:asignatura_id>/<int:alumno_id>/', views.detalle_asistencia, name='detalle_asistencia'),
]
