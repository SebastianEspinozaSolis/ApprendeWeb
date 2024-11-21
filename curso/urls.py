from django.urls import path, include
from . import views

app_name = 'curso'

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('curso/<int:pk>/', views.detalle_curso, name='detalle_curso'),
    path('crear/', views.crear_curso, name='crear_curso'),
    path('editar/<int:pk>/', views.editar_curso, name='editar_curso'),
    path('avisos/', include('avisos.urls', namespace='avisos')),
]
