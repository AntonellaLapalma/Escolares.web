from django.db import models
from apps.empleados.models import *
from apps.vehiculos.models import *

class Gastos_empleado(models.Model):
    id_empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, related_name='id_empleado_gastos')
    fecha = models.DateField(default='2023-01-01')
    total =  models.FloatField()

class Motivos_vehiculo(models.Model):
    motivo=models.CharField(max_length=50)

class Gastos_vehiculo(models.Model):
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, related_name='id_vehiculo_gastos')
    fecha = models.DateField(default='2023-01-01')
    motivo =  models.ForeignKey(Motivos_vehiculo, on_delete=models.SET_NULL, null=True, related_name='motivo_vehiculo_gastos')
    total =  models.FloatField()