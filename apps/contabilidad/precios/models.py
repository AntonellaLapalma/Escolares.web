from django.db import models

class Precio(models.Model):
    tipo = models.CharField(max_length=50)
    total = models.IntegerField()

    def __str__(self):
        return str(self.tipo)