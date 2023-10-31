from django.contrib import admin
from .models import *

@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('id', 'turno', 'tipo' )

@admin.register(Lunes)
class LunesAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'estudiante', 'direccion', 'viaje' )

@admin.register(Martes)
class MartesAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'estudiante', 'direccion', 'viaje' )

@admin.register(Miercoles)
class MiercolesAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'estudiante', 'direccion', 'viaje' )

@admin.register(Jueves)
class JuevesAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'estudiante', 'direccion', 'viaje' )

@admin.register(Viernes)
class ViernesAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'estudiante', 'direccion', 'viaje' )