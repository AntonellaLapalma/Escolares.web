from django.db import models
from ...clientes.familias.models import Familia

class Ingreso(models.Model):
    id_familiar = models.ForeignKey(Familia, on_delete=models.SET_NULL, null=True, related_name='id_familiar_ingresos')
    mes = models.CharField(max_length=50)
    anio = models.CharField(max_length=50)
    descuento =  models.IntegerField()
    total =  models.FloatField()