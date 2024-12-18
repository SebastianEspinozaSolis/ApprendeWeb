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
    path('menu/administrador/', views.menu_administrador, name='menu_administrador'),
    path('menu/profesor/', views.menu_profesor, name='menu_profesor'),
    path('menu_apoderado/', views.menu_apoderado, name='menu_apoderado'),
    path('menu_alumno/', views.menu_alumno, name='menu_alumno'),
    path('alumno/<int:id>/', views.detalle_alumno, name='detalle_alumno'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('editar-foto/', views.editar_foto, name='editar_foto'),
    path('editar-correo/', views.editar_correo, name='editar_correo'),
    path('cambiar-contraseña/', views.cambiar_contraseña, name='cambiar_contraseña'),
    path('editar_administrador/<int:user_id>/', views.editar_administrador, name='editar_administrador'),
    path('editar_profesor/<int:user_id>/', views.editar_profesor, name='editar_profesor'),
    path('editar_apoderado/<int:user_id>/', views.editar_apoderado, name='editar_apoderado'),
    path('editar_alumno/<int:user_id>/', views.editar_alumno, name='editar_alumno'),
    path('borrar_usuario/<int:user_id>/', views.borrar_usuario, name='borrar_usuario'),
]