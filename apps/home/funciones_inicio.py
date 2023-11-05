from apps.contabilidad.ingresos.models import *

class Funciones_Inicio:
    def calcular_recorrdido(self,dia):
        recorridos = 0
        recorridos_1 = dia.objects.filter(viaje__turno='Mañana', viaje__tipo='Ingreso').values('vehiculo').distinct().count()
        recorridos_2 = dia.objects.filter(viaje__turno='Medio dia', viaje__tipo='Salida').values('vehiculo').distinct().count()
        recorridos_3 = dia.objects.filter(viaje__turno='Medio dia', viaje__tipo='Ingreso').values('vehiculo').distinct().count()
        recorridos_4 = dia.objects.filter(viaje__turno='Tarde', viaje__tipo='Salida').values('vehiculo').distinct().count()

        return recorridos_1 + +recorridos_2 + recorridos_3 + recorridos_4
        
        

