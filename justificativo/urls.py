from django.urls import path
from . import views


app_name = 'justificativo'

urlpatterns = [
    path('justificar_asistencia/<int:asistencia_id>/', views.justificar_asistencia, name='justificar_asistencia'),
    path('gestionar_justificativos/', views.gestionar_justificativos, name='gestionar_justificativos'),
]