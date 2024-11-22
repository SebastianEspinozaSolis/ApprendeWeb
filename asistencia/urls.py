from django.urls import path
from . import views

app_name = 'asistencia'

urlpatterns = [
    path('crear/<int:asignatura_id>/', views.crear_asistencia, name='crear_asistencia'),  # Aquí pasamos asignatura_id
    path('editar/<int:asistencia_id>/', views.editar_asistencia, name='editar_asistencia'),
    path('lista_fechas/<int:asignatura_id>/', views.lista_fechas_asistencia, name='lista_fechas_asistencia'),
    path('detalle/<int:asignatura_id>/<int:alumno_id>/', views.detalle_asistencia, name='detalle_asistencia'),
    path('actualizar/<int:asistencia_id>/', views.actualizar_asistencia, name='actualizar_asistencia'),
    path('lista_cursos/', views.lista_cursos, name='lista_cursos'),
]
