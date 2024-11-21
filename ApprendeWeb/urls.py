"""
URL configuration for ApprendeWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static #Importamos la función static de django.conf.urls.static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls', namespace='usuarios')),
    path('curso/', include('curso.urls', namespace='curso')),
    path('asignatura/', include('asignatura.urls', namespace='asignatura')),
    path('evaluacion/', include('evaluacion.urls', namespace='evaluacion')),
    path('calificacion/', include('calificacion.urls', namespace='calificacion')),
    path('jefatura/', include('jefatura.urls', namespace='jefatura')),
    path('avisos/', include('avisos.urls', namespace='avisos')),
    path('asistencia/', include('asistencia.urls', namespace='asistencia')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#Agregamos la ruta para que Django pueda encontrar los archivos multimedia