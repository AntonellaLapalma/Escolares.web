from django.contrib import admin
from .models import *

@admin.register(Motivos_vehiculo)
class MotivoAdmin(admin.ModelAdmin):
    list_display = ('id', 'motivo')
    list_editable = ('motivo',)

@admin.register(Gastos_empleado)
class Gastos_empleadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_empleado','fecha','total')
    list_editable = ( 'id_empleado','fecha','total')

@admin.register(Gastos_vehiculo)
class Gastos_vehiculoAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_vehiculo','fecha','motivo','total')
    list_editable = ( 'id_vehiculo','fecha','motivo','total')