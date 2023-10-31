from django.contrib import admin
from .models import *

@admin.register(Parentesco)
class ParentescoAdmin(admin.ModelAdmin):
    list_display = ('id','parentesco')

@admin.register(Adulto)
class AdultoAdmin(admin.ModelAdmin):
    list_display = ('id','id_familiar','nombre','apellido','parentesco','celular')