from django.shortcuts import render
from apps.home.views import IndexView

class GastosView(IndexView):
    template_name='mostrar_gastos.html'