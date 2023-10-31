from apps.clientes.familias.models import *
from apps.clientes.adultos.models import *
from apps.clientes.estudiantes.models import *
from apps.clientes.direcciones.models import *
from apps.contabilidad.precios.models import *

class Cuota:
    def calcular_cuota(self,cant_ida_o_vuelta, cant_ida_y_vuelta,descuento):
        precio_1_viaje = Precio.objects.get(tipo='Ida o vuelta')
        precio_2_viajes = Precio.objects.get(tipo='Ida y vuelta')
        total = float(cant_ida_o_vuelta) * float(precio_1_viaje.total) + float(cant_ida_y_vuelta) * float(precio_2_viajes.total)
        total= total - ((total/100)*int(descuento))

        return total
    
    def actualizar_cuota(self,id_familia,servicio_contratado,descuento):
        cant_ida_o_vuelta = 0
        cant_ida_y_vuelta = 0
        for servicio in servicio_contratado:
            buscar = Precio.objects.get(id=servicio)
            if buscar.tipo == 'Ida o vuelta':
                cant_ida_o_vuelta+=1
            elif buscar.tipo == 'Ida y vuelta':
                cant_ida_y_vuelta+=1

        familia = Familia.objects.get(id_familiar=id_familia)
        cuota = self.calcular_cuota(cant_ida_o_vuelta, cant_ida_y_vuelta,descuento)
        familia.cuota = cuota
        familia.descuento = descuento
        if cuota > 0:
            familia.estado = True
        if cuota == 0:
            familia.estado = False
        familia.save()

class Registro:
    def registro_adulto(self,familia_id,nombre_adulto,apellido_adulto,parentesco_adulto,celular_adulto):
        if nombre_adulto == '':
            pass
        else:
            familia = Familia.objects.get(id_familiar=familia_id)
            parentesco = Parentesco.objects.get(id=parentesco_adulto)
            adulto = Adulto(id_familiar=familia, nombre=nombre_adulto, apellido=apellido_adulto, parentesco=parentesco, celular=celular_adulto)
            adulto.save()

    def registro_estudiante(self,familia_id,nombre_estudiante,apellido_estudiante,nvl_estudiante,nvl_num_estudiante,division_estudiante,turno_estudiante,viaje):
        if nombre_estudiante == '':
            pass
        else:
            familia = Familia.objects.get(id_familiar=familia_id)
            nvl_educativo = Nvl_educativo.objects.get(id=nvl_estudiante)
            division = Division.objects.get(id=division_estudiante)
            turno =  Turno.objects.get(id=turno_estudiante)
            if viaje != 'Ninguno':
                viaje_b = Precio.objects.get(id=viaje)
                viaje = viaje_b
            estudiante = Estudiante(id_familiar=familia, nombre=nombre_estudiante, apellido=apellido_estudiante, nvl_educativo=nvl_educativo, sala_grado_anio=nvl_num_estudiante, division=division,
            turno=turno,viaje=viaje)
            estudiante.save()

    def registro_direccion(self,familia_id,calle,altura,piso,dpto):
        if calle == '':
            pass
        else:
            familia = Familia.objects.get(id_familiar=familia_id)
            direccion = Direccion(id_familiar=familia, calle=calle, altura=altura, piso=piso, dpto=dpto)
            direccion.save()

class Modificar:
    def modificar_adulto(self,id_adulto,adulto_nombre,adulto_apellido,adulto_parentesco,adulto_celular):
        try:
            adulto = Adulto.objects.get(id=id_adulto)
            parentesco = Parentesco.objects.get(id=adulto_parentesco)
            adulto.nombre = adulto_nombre
            adulto.apellido = adulto_apellido
            adulto.parentesco = parentesco
            adulto.celular = adulto_celular
            adulto.save()
            return True
        except Adulto.DoesNotExist:
            return False 

    def modificar_estudiante(self,id_estudiante,estudiante_nombre,estudiante_apellido,estudiante_nvl_educativo,estudiante_nvl_num,estudiante_division,estudiante_turno,viaje):
        try:
            estudiante = Estudiante.objects.get(id=id_estudiante)
            nvl_educativo = Nvl_educativo.objects.get(id=estudiante_nvl_educativo)
            division = Division.objects.get(id=estudiante_division)
            turno =  Turno.objects.get(id=estudiante_turno)
            if viaje != 'Ninguno':
                viaje = Precio.objects.get(id=viaje)

            estudiante.nombre = estudiante_nombre
            estudiante.apellido = estudiante_apellido
            estudiante.nvl_educativo = nvl_educativo
            estudiante.sala_grado_anio = estudiante_nvl_num
            estudiante.division = division
            estudiante.turno = turno
            estudiante.viaje=viaje
            estudiante.save()
            return True
        except Estudiante.DoesNotExist:
            return False 
        
    def modificar_direccion(self,id_direccion,direccion_calle, direccion_altura,direccion_piso,direccion_dpto):
        try:
            direccion = Direccion.objects.get(id=id_direccion)
            direccion.calle = direccion_calle
            direccion.altura = direccion_altura
            direccion.piso = direccion_piso
            direccion.dpto = direccion_dpto
            direccion.save()
            return True
        except Direccion.DoesNotExist:
            return False  

class Eliminar:
    def eliminar_adulto(self, id_adulto):
        try:
            adulto = Adulto.objects.get(id=id_adulto)
            adulto.delete()
            return True  
        except Adulto.DoesNotExist:
            return False  

    def eliminar_estudiante(self, id_estudiante):
        try:
            estudiante = Estudiante.objects.get(id=id_estudiante)
            estudiante.delete()
            return True  
        except Estudiante.DoesNotExist:
            return False  

    def eliminar_direccion(self, id_direccion):
        try:
            direccion = Direccion.objects.get(id=id_direccion)
            direccion.delete()
            return True  
        except Direccion.DoesNotExist:
            return False  
        
class Validaciones_C:
    def cadena_alfabetica(self,cadena):
        return all(caracter.isalpha() or caracter.isspace() for caracter in cadena)
    
    def cadena_numerica(self,cadena):
        return cadena.isdigit()

    def validar_nombre(self,nombre):
        nombre_error = None
        val=self.cadena_alfabetica(nombre)
        if not val and nombre != '':
            nombre_error = 'Ingrese solo letras.*'
        if nombre == '':
            pass
        return nombre_error
        
    def validar_celular_r(self,celular):
        celular_error = None
        if not celular.isdigit() and celular != '':
            celular_error = 'Ingrese un celular válido.*'
        elif celular.isdigit():
            try:
                Adulto.objects.get(celular=celular)
                return 'Celular en uso.*'
            except:
                return celular_error
        if celular == '':
            pass
        return celular_error
    
    def validar_parentesco(self,parentesco):
        if parentesco != '' and parentesco != None:
            try:
                parentesco= Parentesco.objects.get(id=parentesco)
                return None
            except:
                return 'Elija una opción válida.*'
    
    def validar_celular_m(self,celular,id):
        celular_error = None
        if not celular.isdigit():
            celular_error = 'Ingrese un celular válido.*'
        elif celular.isdigit():
            try:
                b = Adulto.objects.get(celular=celular)
                if int(b.id)==int(id):
                    return None
                else:
                    celular_error = 'El número ya se encuentra registrado.*'
            except Adulto.DoesNotExist:
                pass

        if celular == '':
            pass

        return celular_error
    
    def validar_calle(self,calle):
        calle_error = None
        resultado = all(caracter.isalpha() or caracter.isspace() or caracter.isdigit() for caracter in calle)
        if not resultado:
            calle_error = 'Ingrese letras y/o números.*'
        return calle_error
    
    def validar_altura(self,altura):
        altura_error = None
        if not altura.isdigit() and altura != '':
            altura_error = 'Ingrese una altura válida.*'
        return altura_error
    
    def validar_piso(self,piso):
        piso_error = None
        if not piso.isdigit() and piso != '':
            piso_error = 'Ingrese un piso válido.*'
        return piso_error
    
    def validar_dpto(self,dpto):
        val=all(caracter.isalpha() or caracter.isdigit() for caracter in dpto)
        if not val:
            return'Ingrese números y/o letras.'
        return None
    
    def validar_nvl(self,nvl):
        e=None
        if nvl != '' and nvl != None:
            try:
                Nvl_educativo.objects.get(id=nvl)
                return e
            except:
                e='Error.*'
                return 
        
    def validar_nvl_num(self,nvl,nvl_num):
        e = None
        if nvl_num != '' and nvl_num is not None:
            print(nvl_num)
            try:
                print(nvl)
                buscar = Nvl_educativo.objects.get(id=nvl)
                print(buscar.inicio, buscar.fin)
                if int(buscar.inicio) <= int(nvl_num)  <= int(buscar.fin):
                    e = None
                else:
                    e = 'Error.*'
            except Nvl_educativo.DoesNotExist:
                e = 'Error.*'
        else:
            e = None

        return e
        
    def validar_division(self,div):
        e=None
        if div != '' and div != None:
            try:
                Division.objects.get(id=div)
                return e
            except:
                e='Error.*'
                return 
        
    def validar_turno(self,turno):
        e=None
        if turno != '' and turno != None:
            try:
                Turno.objects.get(id=turno)
                return e
            except:
                e='Error.*'
                return 
        
    def validar_servicio(self,servicio):
        e=None
        if servicio != '' and servicio != None:
            try:
                Precio.objects.get(id=servicio)
                return e
            except:
                e='Error.*'
                return 
