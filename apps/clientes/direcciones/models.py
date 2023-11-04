from django.db import models
from ..familias.models import Familia

class Direccion(models.Model):
    id_familiar = models.ForeignKey(Familia, on_delete=models.CASCADE)
    calle = models.CharField(max_length=80)
    altura = models.CharField(max_length=20)
    piso = models.CharField(max_length=20)
    dpto = models.CharField(max_length=20)