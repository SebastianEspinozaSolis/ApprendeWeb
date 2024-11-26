from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('crear_administrador/<int:user_id>/', views.crear_administrador, name='crear_administrador'),
    path('crear_apoderado/<int:user_id>/', views.crear_apoderado, name='crear_apoderado'),
    path('crear_alumno/<int:user_id>/', views.crear_alumno, name='crear_alumno'),
    path('crear_profesor/<int:user_id>/', views.crear_profesor, name='crear_profesor'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
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
    path('pomodoro/', views.pomodoro_view, name='pomodoro'),
    path('actualizar-datos-alumno/<int:alumno_id>/', views.actualizar_datos_alumno, name='actualizar_datos_alumno'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)