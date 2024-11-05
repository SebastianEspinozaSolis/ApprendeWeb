from django.urls import path
from . import views

app_name = 'calificacion'

urlpatterns = [
    path('crear/', views.crear_calificacion, name='crear_calificacion'),
    path('editar/<int:pk>/', views.editar_calificacion, name='editar_calificacion'), 
]