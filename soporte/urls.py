from django.urls import path
from . import views

app_name = 'soporte'  

urlpatterns = [
    path('reportar/', views.crear_reporte, name='crear_reporte'),
]
