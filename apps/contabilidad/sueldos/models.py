from django.db import models

class Puesto(models.Model):
    puesto = models.CharField(primary_key=True,max_length=20)
    sueldo = models.FloatField()