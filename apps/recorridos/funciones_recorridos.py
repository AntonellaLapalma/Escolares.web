from django.db.models import Q
from apps.recorridos.models import *
from apps.vehiculos.models import Vehiculo
from apps.clientes.estudiantes.models import *

class FuncionesLunes:
    def filtrar_lunes(self,vehiculo_seleccionado,turno,tipo):
        vehiculo = Vehiculo.objects.get(id=vehiculo_seleccionado)

        resultado_lunes = Lunes.objects.filter(vehiculo=vehiculo.id, viaje__turno=turno, viaje__tipo=tipo)

        turno_filtro = Precio.objects.get(tipo='Ida o vuelta')

        # Primero filtro los datos para obtener solo los estudiantes sin recorrido y con servicio contratado
        estudiantes_con_recorrido= [r.estudiante.id for r in resultado_lunes]
        estudiantes_sin_recorrido = Estudiante.objects.exclude(
            Q(id__in=estudiantes_con_recorrido) | Q(viaje__tipo='Ninguno') # utilizo or 
        )
        # Busco que no viaje en otro turno en caso de haber contratado ida o vuelta y ya este haciendo uso de 1
        estudiantes_sin_filtrar_viaje = Lunes.objects.filter(vehiculo=vehiculo.id,estudiante__viaje__id=turno_filtro.id)
        estudiantes_sin_filtrar_viaje_lista= [r.estudiante.id for r in estudiantes_sin_filtrar_viaje]

        # Excluyo los estudiantes que tienen 'ida o vuelta' y se encuentran viajando en otro turno
        estudiantes_sin_recorrido2 = estudiantes_sin_recorrido.exclude(id__in=estudiantes_sin_filtrar_viaje_lista,viaje__id=turno_filtro.id)

        return estudiantes_sin_recorrido2
    
    def lugares_disponibles_l(self,vehiculo_seleccionado,turno,tipo):
        vehiculo = Vehiculo.objects.get(id=vehiculo_seleccionado)
        resultado_lunes = Lunes.objects.filter(vehiculo=vehiculo.id, viaje__turno=turno, viaje__tipo=tipo)
        numero_de_resultados = resultado_lunes.count()

        if numero_de_resultados >= int(vehiculo.cant_asientos):
            return False
        else:
            return True

class FuncionesMartes:
    def filtrar_martes(self,vehiculo_seleccionado,turno,tipo):
        vehiculo = Vehiculo.objects.get(id=vehiculo_seleccionado)

        resultado_martes = Martes.objects.filter(vehiculo=vehiculo.id, viaje__turno=turno, viaje__tipo=tipo)

        turno_filtro = Precio.objects.get(tipo='Ida o vuelta')

        # Primero filtro los datos para obtener solo los estudiantes sin recorrido y con servicio contratado
        estudiantes_con_recorrido= [r.estudiante.id for r in resultado_martes]
        estudiantes_sin_recorrido = Estudiante.objects.exclude(
            Q(id__in=estudiantes_con_recorrido) | Q(viaje__tipo='Ninguno') # utilizo or 
        )
        # Busco que no viaje en otro turno en caso de haber contratado ida o vuelta y ya este haciendo uso de 1
        estudiantes_sin_filtrar_viaje = Martes.objects.filter(vehiculo=vehiculo.id,estudiante__viaje__id=turno_filtro.id)
        estudiantes_sin_filtrar_viaje_lista= [r.estudiante.id for r in estudiantes_sin_filtrar_viaje]

        # Excluyo los estudiantes que tienen 'ida o vuelta' y se encuentran viajando en otro turno
        estudiantes_sin_recorrido2 = estudiantes_sin_recorrido.exclude(id__in=estudiantes_sin_filtrar_viaje_lista,viaje__id=turno_filtro.id)

        return estudiantes_sin_recorrido2
    
    def lugares_disponibles_m(self,vehiculo_seleccionado,turno,tipo):
        vehiculo = Vehiculo.objects.get(id=vehiculo_seleccionado)
        resultado_martes = Martes.objects.filter(vehiculo=vehiculo.id, viaje__turno=turno, viaje__tipo=tipo)
        numero_de_resultados = resultado_martes.count()

        if numero_de_resultados >= int(vehiculo.cant_asientos):
            return False
        else:
            return True

class FuncionesMiercoles:
    def filtrar_miercoles(self,vehiculo_seleccionado,turno,tipo):
        vehiculo = Vehiculo.objects.get(id=vehiculo_seleccionado)

        resultado_miercoles = Miercoles.objects.filter(vehiculo=vehiculo.id, viaje__turno=turno, viaje__tipo=tipo)

        turno_filtro = Precio.objects.get(tipo='Ida o vuelta')

        # Primero filtro los datos para obtener solo los estudiantes sin recorrido y con servicio contratado
        estudiantes_con_recorrido= [r.estudiante.id for r in resultado_miercoles]
        estudiantes_sin_recorrido = Estudiante.objects.exclude(
            Q(id__in=estudiantes_con_recorrido) | Q(viaje__tipo='Ninguno') # utilizo or 
        )
        # Busco que no viaje en otro turno en caso de haber contratado ida o vuelta y ya este haciendo uso de 1
        estudiantes_sin_filtrar_viaje = Miercoles.objects.filter(vehiculo=vehiculo.id,estudiante__viaje__id=turno_filtro.id)
        estudiantes_sin_filtrar_viaje_lista= [r.estudiante.id for r in estudiantes_sin_filtrar_viaje]

        # Excluyo los estudiantes que tienen 'ida o vuelta' y se encuentran viajando en otro turno
        estudiantes_sin_recorrido2 = estudiantes_sin_recorrido.exclude(id__in=estudiantes_sin_filtrar_viaje_lista,viaje__id=turno_filtro.id)

        return estudiantes_sin_recorrido2
    
    def lugares_disponibles_x(self,vehiculo_seleccionado,turno,tipo):
        vehiculo = Vehiculo.objects.get(id=vehiculo_seleccionado)
        resultado_miercoles = Miercoles.objects.filter(vehiculo=vehiculo.id, viaje__turno=turno, viaje__tipo=tipo)
        numero_de_resultados = resultado_miercoles.count()

        if numero_de_resultados >= int(vehiculo.cant_asientos):
            return False
        else:
            return True
    
class FuncionesJueves:
    def filtrar_jueves(self,vehiculo_seleccionado,turno,tipo):
        vehiculo = Vehiculo.objects.get(id=vehiculo_seleccionado)

        resultado_jueves = Jueves.objects.filter(vehiculo=vehiculo.id, viaje__turno=turno, viaje__tipo=tipo)

        turno_filtro = Precio.objects.get(tipo='Ida o vuelta')

        # Primero filtro los datos para obtener solo los estudiantes sin recorrido y con servicio contratado
        estudiantes_con_recorrido= [r.estudiante.id for r in resultado_jueves]
        estudiantes_sin_recorrido = Estudiante.objects.exclude(
            Q(id__in=estudiantes_con_recorrido) | Q(viaje__tipo='Ninguno') # utilizo or 
        )
        # Busco que no viaje en otro turno en caso de haber contratado ida o vuelta y ya este haciendo uso de 1
        estudiantes_sin_filtrar_viaje = Jueves.objects.filter(vehiculo=vehiculo.id,estudiante__viaje__id=turno_filtro.id)
        estudiantes_sin_filtrar_viaje_lista= [r.estudiante.id for r in estudiantes_sin_filtrar_viaje]

        # Excluyo los estudiantes que tienen 'ida o vuelta' y se encuentran viajando en otro turno
        estudiantes_sin_recorrido2 = estudiantes_sin_recorrido.exclude(id__in=estudiantes_sin_filtrar_viaje_lista,viaje__id=turno_filtro.id)

        return estudiantes_sin_recorrido2
    
    def lugares_disponibles_j(self,vehiculo_seleccionado,turno,tipo):
        vehiculo = Vehiculo.objects.get(id=vehiculo_seleccionado)
        resultado_jueves = Jueves.objects.filter(vehiculo=vehiculo.id, viaje__turno=turno, viaje__tipo=tipo)
        numero_de_resultados = resultado_jueves.count()

        if numero_de_resultados >= int(vehiculo.cant_asientos):
            return False
        else:
            return True

class FuncionesViernes:
    def filtrar_viernes(self,vehiculo_seleccionado,turno,tipo):
        vehiculo = Vehiculo.objects.get(id=vehiculo_seleccionado)

        resultado_viernes = Viernes.objects.filter(vehiculo=vehiculo.id, viaje__turno=turno, viaje__tipo=tipo)

        turno_filtro = Precio.objects.get(tipo='Ida o vuelta')

        # Primero filtro los datos para obtener solo los estudiantes sin recorrido y con servicio contratado
        estudiantes_con_recorrido= [r.estudiante.id for r in resultado_viernes]
        estudiantes_sin_recorrido = Estudiante.objects.exclude(
            Q(id__in=estudiantes_con_recorrido) | Q(viaje__tipo='Ninguno') # utilizo or 
        )
        # Busco que no viaje en otro turno en caso de haber contratado ida o vuelta y ya este haciendo uso de 1
        estudiantes_sin_filtrar_viaje = Viernes.objects.filter(vehiculo=vehiculo.id,estudiante__viaje__id=turno_filtro.id)
        estudiantes_sin_filtrar_viaje_lista= [r.estudiante.id for r in estudiantes_sin_filtrar_viaje]

        # Excluyo los estudiantes que tienen 'ida o vuelta' y se encuentran viajando en otro turno
        estudiantes_sin_recorrido2 = estudiantes_sin_recorrido.exclude(id__in=estudiantes_sin_filtrar_viaje_lista,viaje__id=turno_filtro.id)

        return estudiantes_sin_recorrido2

    def lugares_disponibles_v(self,vehiculo_seleccionado,turno,tipo):
        vehiculo = Vehiculo.objects.get(id=vehiculo_seleccionado)
        resultado_viernes = Viernes.objects.filter(vehiculo=vehiculo.id, viaje__turno=turno, viaje__tipo=tipo)
        numero_de_resultados = resultado_viernes.count()

        if numero_de_resultados >= int(vehiculo.cant_asientos):
            return False
        else:
            return True 
