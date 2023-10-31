from django.contrib import admin
from .models import *

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('id','id_familiar','nombre','apellido','nvl_educativo','sala_grado_anio', 'division', 'turno', 'viaje')

@admin.register(Nvl_educativo)
class Nvl_educativoAdmin(admin.ModelAdmin):
    list_display = ('id','tipo', 'inicio', 'fin')

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_nvl_educativo', 'division')

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('id','turno')