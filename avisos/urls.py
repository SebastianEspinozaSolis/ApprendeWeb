from django.urls import path
from . import views

app_name = 'avisos'

urlpatterns = [
    path('crear-aviso/<int:curso_id>/', views.crear_aviso, name='crear_aviso'), 
    path('seleccionar-curso/', views.seleccionar_curso, name='seleccionar_curso'),
    path('lista-avisos/', views.lista_avisos, name='lista_avisos'),
    path('detalle-aviso/<int:aviso_id>/', views.detalle_aviso, name='detalle_aviso'),
    path('editar-aviso/<int:aviso_id>/', views.editar_aviso, name='editar_aviso'),
    path('avisos-apoderado/', views.avisos_apoderado, name='avisos_apoderado'),
    path('mis-avisos/', views.mis_avisos, name='mis_avisos'), 
]
