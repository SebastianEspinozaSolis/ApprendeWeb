from django.urls import path
from . import views

app_name = 'asignatura'

urlpatterns = [
    path('', views.lista_asignaturas, name='lista_asignaturas'),
    path('curso/<int:curso_id>/', views.lista_asignaturas, name='lista_asignaturas_curso'),
    path('asignatura/<int:pk>/', views.detalle_asignatura, name='detalle_asignatura'),
    path('crear/<int:curso_id>/', views.crear_asignatura, name='crear_asignatura'),
    path('editar/<int:pk>/', views.editar_asignatura, name='editar_asignatura'),
]