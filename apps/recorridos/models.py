from django.db import models
from ..vehiculos.models import Vehiculo
from ..clientes.estudiantes.models import Estudiante
from ..clientes.direcciones.models import Direccion

class Viaje(models.Model):
    turno = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)

class Lunes(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='vehiculo_lunes')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='pasajero_lunes')
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, related_name='direccion_pasajero_lunes')
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)

class Martes(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='vehiculo_martes')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='pasajero_martes')
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, related_name='direccion_pasajero_martes')
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)

class Miercoles(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='vehiculo_miercoles')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='pasajero_miercoles')
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, related_name='direccion_pasajero_miercoles')
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)

class Jueves(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='vehiculo_jueves')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='pasajero_jueves')
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, related_name='direccion_pasajero_jueves')
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)

class Viernes(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='vehiculo_viernes')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='pasajero_viernes')
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, related_name='direccion_pasajero_viernes')
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)
    