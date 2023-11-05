from apps.empleados.models import *
from apps.recorridos.models import *
from apps.vehiculos.models import *

class Validar_Ingresos:
    def validar_nombre_empleado(self,nombre):
        nombre_error = None
        if not nombre:
            nombre_error = 'Ingrese un nombre.*'
        elif not self.es_letras_y_espacios(nombre):
            nombre_error = 'Ingrese solo letras.*'
        return nombre_error
    
    def validar_apellido_empleado(self,apellido):
        apellido_error = None
        if not apellido:
            apellido_error = 'Ingrese un apellido.*'
        elif not self.es_letras_y_espacios(apellido):
            apellido_error = 'Ingrese solo letras.*'
        return apellido_error
    
    def validar_celular_empleado(self,celular):
        celular_error = None
        
        if not celular.isdigit():
            celular_error = 'Ingrese un celular válido.*'
        elif celular.isdigit():
            val=self.validar_inexistencia_empleado(celular)
            if val:
                celular_error = 'El número ya se encuentra registrado.*'
        return celular_error
    
    def validar_celular_modificacion(self,celular,id):
        celular_error = None
        
        if not celular.isdigit():
            celular_error = 'Ingrese un celular válido.*'
        elif celular.isdigit():
            try:
                empleado = Empleado.objects.get(celular=celular)
                if int(empleado.id) != int(id):
                    celular_error = 'El número ya se encuentra registrado.*'

            except Empleado.DoesNotExist:    
                pass
                
        return celular_error
    
    def es_letras_y_espacios(self,cadena):
        return all(caracter.isalpha() or caracter.isspace() for caracter in cadena)
    
    def validar_inexistencia_empleado(self,num):
        empleado = Empleado.objects.filter(celular=num)

        if empleado.exists():
            return True
        else:
            return False
