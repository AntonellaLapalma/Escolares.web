from django.db import models
from ..contabilidad.sueldos.models import Puesto

class Empleado(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    celular = models.CharField(max_length=20)
    puesto = models.ForeignKey(Puesto, on_delete=models.CASCADE, related_name='chofer_puesto', null=True, blank=True)