from django.urls import path
from . import views

app_name = 'jefatura'

urlpatterns = [
    path('crear/', views.crear_jefatura, name='crear_jefatura'),
    path('', views.lista_jefaturas, name='lista_jefaturas'), 
    path('editar/<int:pk>/', views.editar_jefatura, name='editar_jefatura'),
]