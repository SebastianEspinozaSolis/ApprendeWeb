from django.contrib import admin
from .models import Reporte

# Registrar el modelo Reporte en el admin
@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'tipo', 'fecha_creacion', 'usuario')
    search_fields = ('titulo', 'descripcion', 'tipo')
    list_filter = ('tipo', 'fecha_creacion')