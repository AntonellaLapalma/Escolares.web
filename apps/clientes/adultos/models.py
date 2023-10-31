from django.db import models
from ..familias.models import Familia

class Parentesco(models.Model):
    parentesco = models.CharField(max_length=50)

    def __str__(self):
        return str(self.parentesco)

class Adulto(models.Model):
    id_familiar = models.ForeignKey(Familia, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    parentesco = models.ForeignKey(Parentesco, on_delete=models.SET_NULL, null=True)
    celular = models.CharField(max_length=20)