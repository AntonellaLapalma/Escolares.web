from django.contrib import admin

# Register your models here.

from .models import *

@admin.register(Ingreso)
class IngresoAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_familiar', 'fecha', 'descuento', 'total' )