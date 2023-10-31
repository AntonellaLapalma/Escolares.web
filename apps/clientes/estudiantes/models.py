from django.db import models
from ..familias.models import Familia
from ...contabilidad.precios.models import Precio

class Nvl_educativo(models.Model):
    tipo = models.CharField(max_length=50)
    inicio = models.IntegerField()
    fin = models.IntegerField()

    def __str__(self):
        return str(self.tipo)

class Division(models.Model):
    id_nvl_educativo = models.ForeignKey(Nvl_educativo, on_delete=models.CASCADE)
    division = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id_nvl_educativo.tipo)
   
class Turno(models.Model):
    turno = models.CharField(max_length=50)

    def __str__(self):
        return str(self.turno)

class Estudiante(models.Model):
    id_familiar = models.ForeignKey(Familia, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    nvl_educativo = models.ForeignKey(Nvl_educativo, on_delete=models.SET_NULL, null=True)
    sala_grado_anio = models.CharField(max_length=50)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True)
    turno = models.ForeignKey(Turno, on_delete=models.SET_NULL, null=True)
    viaje = models.ForeignKey(Precio, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.id)