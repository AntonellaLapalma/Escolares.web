from django.shortcuts import render
from apps.home.views import IndexView

class IngresosView(IndexView):
    template_name='mostrar_ingresos.html'