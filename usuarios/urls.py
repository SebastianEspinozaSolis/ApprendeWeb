from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('crear_administrador/<int:user_id>/', views.crear_administrador, name='crear_administrador'),
    path('crear_apoderado/<int:user_id>/', views.crear_apoderado, name='crear_apoderado'),
    path('crear_alumno/<int:user_id>/', views.crear_alumno, name='crear_alumno'),
    path('crear_profesor/<int:user_id>/', views.crear_profesor, name='crear_profesor'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('lista_usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('editar_usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('detalle_usuario/<int:pk>/', views.detalle_usuario, name='detalle_usuario'), 
]