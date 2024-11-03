from django.urls import path
from . import views

app_name = 'calificacion'

urlpatterns = [
    path('', views.lista_calificaciones, name='lista_calificaciones'),
    path('calificacion/<int:pk>/', views.detalle_calificacion, name='detalle_calificacion'),
    path('crear/', views.crear_calificacion, name='crear_calificacion'),
    path('editar/<int:pk>/', views.editar_calificacion, name='editar_calificacion'),
]