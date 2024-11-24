from django.urls import path
from . import views

app_name = 'evaluacion'

urlpatterns = [
    path('evaluacion/<int:pk>/', views.detalle_evaluacion, name='detalle_evaluacion'),
    path('crear/', views.crear_evaluacion, name='crear_evaluacion'),
    path('editar/<int:pk>/', views.editar_evaluacion, name='editar_evaluacion'),
]
