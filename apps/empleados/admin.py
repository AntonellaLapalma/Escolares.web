from django.contrib import admin
from .models import *

@admin.register(Puesto)
class PuestoAdmin(admin.ModelAdmin):
    list_display = ('puesto', 'sueldo')
    list_editable = ('sueldo',)

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'celular', 'puesto')
    list_editable = ('nombre', 'apellido', 'celular', 'puesto')
