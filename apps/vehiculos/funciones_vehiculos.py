from apps.empleados.models import Empleado
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from django.db.models import Q


class Validar_Ingresos_v:
    def validar_patente_r(self,patente):
        patente_error = None
        val=all(caracter.isalpha() or caracter.isdigit() for caracter in patente)

        inex=self.validar_inexistencia_vehiculo(patente)
        if not val:
            patente_error = 'Error, patente Inválida.*'
        elif patente == '':
            patente_error = 'Ingrese una patente.*'
        elif val:
            if inex:
                patente_error = 'La patente está en uso.*'
        
        return patente_error
    def validar_patente_m(self,patente,id):
        patente_error = None
        val=all(caracter.isalpha() or caracter.isdigit() for caracter in patente)
        vehiculo_actual=Vehiculo.objects.get(id=id)
        if vehiculo_actual.patente != patente:
            inex=self.validar_inexistencia_vehiculo(patente)
        else:
            inex=False
        if not val:
            patente_error = 'Error, patente Inválida.*'
        elif patente == '':
            patente_error = 'Ingrese una patente.*'
        elif val:
            if inex:
                patente_error = 'La patente está en uso.*'
        
        return patente_error

    def validar_asientos(self,asiento):
        asiento_error = None
        
        if not asiento.isdigit():
            asiento_error = 'Ingrese solo números.*'
        
        return asiento_error
    
    def validar_existencia_chofer(self,id):
        if id != 'Ninguno':
            if id.isdigit():    
                try:
                    Empleado.objects.get(id=id, puesto__puesto='Chofer')
                    return True
                except ObjectDoesNotExist:
                    return False
            else:
                return False

    def validar_existencia_celador(self,id):
        if id != 'Ninguno':
            try:
                Empleado.objects.get(id=id, puesto__puesto='Celador')
                return True
            except ObjectDoesNotExist:
                return False

    def validar_inexistencia_vehiculo(self,num):
        vehiculo = Vehiculo.objects.filter(patente=num)

        if vehiculo.exists():
            return True
        else:
            return False
    
class Traer_Datos:
    def empleados_libres(self):
        empleados = Empleado.objects.all()

        # Traigo todos los empleados que estan asignados como chofer o celador
        empleados_asignados = Empleado.objects.filter(
            Q(chofer_de_vehiculo__isnull=False) | 
            Q(celador_de_vehiculo__isnull=False)
        ).distinct()

        # Excluyo los empleados asignados de la lista original
        empleados_sin_asignar = empleados.exclude(id__in=empleados_asignados)   
        return empleados_sin_asignar