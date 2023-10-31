from django.db import models

class Familia(models.Model):
    # Esta tabla se usara para crear los id familiares que se utilizaran en el resto de tablas pertenecientes a la seccion clientes 
    id_familiar = models.BigAutoField(primary_key=True)
    estado = models.BooleanField(default=False)
    cuota = models.FloatField(default=0)
    descuento = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id_familiar)