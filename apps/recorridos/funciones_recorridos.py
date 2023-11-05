from django.db.models import Q
from apps.recorridos.models import *
from apps.vehiculos.models import Vehiculo
from apps.clientes.estudiantes.models import *

class Funciones_Recorridos:
    def filtrar(self,dia,vehiculo_seleccionado,turno,tipo):
        vehiculo = Vehiculo.objects.get(id=vehiculo_seleccionado)

        resultados = dia.objects.filter(viaje__turno=turno, viaje__tipo=tipo) # traigo los resultados que sean igual al turno

        turno_filtro = Precio.objects.get(tipo='Ida o vuelta')

        # Primero filtro los datos para obtener solo los estudiantes sin recorrido y con servicio contratado
        estudiantes_con_recorrido= [r.estudiante.id for r in resultados]
        estudiantes_sin_recorrido = Estudiante.objects.exclude(
            Q(id__in=estudiantes_con_recorrido) | Q(viaje__tipo='Ninguno') # utilizo or 
        )
        # Busco que no viaje en otro turno en caso de haber contratado ida o vuelta y ya este haciendo uso de 1
        estudiantes_sin_filtrar_viaje = dia.objects.filter(vehiculo=vehiculo.id,estudiante__viaje__id=turno_filtro.id)
        estudiantes_sin_filtrar_viaje_lista= [r.estudiante.id for r in estudiantes_sin_filtrar_viaje]

        # Excluyo los estudiantes que tienen 'ida o vuelta' y se encuentran viajando en otro turno
        estudiantes_sin_recorrido2 = estudiantes_sin_recorrido.exclude(id__in=estudiantes_sin_filtrar_viaje_lista,viaje__id=turno_filtro.id)

        return estudiantes_sin_recorrido2
    
    def lugares_disponibles(self,dia,vehiculo_seleccionado,turno,tipo):
        vehiculo = Vehiculo.objects.get(id=vehiculo_seleccionado)
        resultado_lunes = dia.objects.filter(vehiculo=vehiculo.id, viaje__turno=turno, viaje__tipo=tipo)
        numero_de_resultados = resultado_lunes.count()

        if numero_de_resultados >= int(vehiculo.cant_asientos):
            return False
        else:
            return True

    def crear_mensaje(self,vehiculo,dia,turno,tipo):
        vehiculo = Vehiculo.objects.get(id=vehiculo)
        turno = Viaje.objects.get(turno=turno,tipo=tipo)
        pasajeros = dia.objects.filter(vehiculo=vehiculo,viaje=turno)

        listado = ''
        for pasajero in pasajeros:
            nombre = f"{pasajero.estudiante.nombre}{pasajero.estudiante.apellido}"
            elemento = f"{pasajero.estudiante.nvl_educativo} {pasajero.estudiante.sala_grado_anio} {pasajero.estudiante.division.division}%0A{pasajero.direccion.calle} {pasajero.direccion.altura} {pasajero.direccion.piso} {pasajero.direccion.dpto}"

            listado += f"{nombre}%0A{elemento}%0A%0A"
        print(listado)
        
        return listado