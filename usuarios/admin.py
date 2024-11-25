from django.contrib import admin
from .models import Perfil, Administrador 

# Register your models here. 

class PerfilAdmin(admin.ModelAdmin): 
    list_display=["rol","nombre","rut","fecha_nacimiento","sexo"] 
class AdministradorAdmin(admin.ModelAdmin):
    list_display=["cargo"]
 
admin.site.register(Perfil,PerfilAdmin) 
admin.site.register(Administrador,AdministradorAdmin)