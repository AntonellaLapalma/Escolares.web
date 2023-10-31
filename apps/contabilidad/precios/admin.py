from django.contrib import admin
from .models import *

@admin.register(Precio)
class PrecioAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'total' )