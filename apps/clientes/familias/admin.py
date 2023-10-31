from django.contrib import admin
from .models import *

@admin.register(Familia)
class FamiliaAdmin(admin.ModelAdmin):
    list_display = ('id_familiar', 'estado', 'cuota','descuento')