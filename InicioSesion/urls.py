from django.urls import path
from . import views
app_name = 'iniciosesion'
urlpatterns = [
 path('', views.iniciosesion, name='iniciosesion'),
]
