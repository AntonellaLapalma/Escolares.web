from django.db import models
from ..empleados.models import Empleado

class Vehiculo(models.Model):
    patente = models.CharField(max_length=20)
    cant_asientos = models.CharField(max_length=50)
    chofer = models.ForeignKey(Empleado, on_delete=models.SET_NULL, related_name='chofer_de_vehiculo', null=True, blank=True)
    celador = models.ForeignKey(Empleado, on_delete=models.SET_NULL, related_name='celador_de_vehiculo', null=True, blank=True)