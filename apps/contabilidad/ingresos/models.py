from django.db import models
from apps.clientes.familias.models import Familia

class Ingreso(models.Model):
    id_familiar = models.ForeignKey(Familia, on_delete=models.SET_NULL, null=True, related_name='id_familiar_ingresos')
    fecha = models.DateField(default='2023-01-01')
    descuento =  models.IntegerField()
    total =  models.FloatField()