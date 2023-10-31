from django.contrib import admin
from .models import *

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('id', 'patente' ,'cant_asientos', 'chofer', 'celador' )