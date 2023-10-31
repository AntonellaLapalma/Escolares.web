from django.contrib import admin
from .models import *

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('id','id_familiar','calle', 'altura', 'piso','dpto')