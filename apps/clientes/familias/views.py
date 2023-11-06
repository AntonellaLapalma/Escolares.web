from django.shortcuts import render, redirect
from apps.home.views import IndexView
from django.views import View
from apps.clientes.adultos.models import *
from apps.clientes.estudiantes.models import *
from apps.clientes.direcciones.models import *
from apps.contabilidad.precios.models import *
from django.db.models import Q
from apps.clientes.familias.funciones_cliente import *
from django.http import JsonResponse


class ClientesView(IndexView):
    template_name = 'mostrar_clientes.html'

    def get(self, request, *args, **kwargs):
        # En caso de que no se haya iniciado sesion redirige a login
        if not request.user.is_authenticated:
            return redirect('login')

        # Llamo al metodo get_context_data y paso los resultados
        context = self.get_context_data()
        return render(request, self.template_name, context)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtengo el valor del 'estado' en la URL
        estado = self.kwargs.get('estado')

        # Si esta presente, filtro
        if estado == 'activo':
            familias = Familia.objects.exclude(estado=False)
        elif estado == 'inactivo':
            familias = Familia.objects.filter(estado=False)
        else:
            # Si no obtengo todos
            familias = Familia.objects.all()

        # Obtengo el valor del parametro 'busqueda' en la URL
        busqueda = self.request.GET.get('busqueda', '')

        adultos = Adulto.objects.all()
        estudiantes = Estudiante.objects.all()
       
        if busqueda:
            try:
                busqueda_int = int(busqueda)
                adultos = adultos.filter(
                    Q(id_familiar=busqueda_int) |
                    Q(celular=busqueda_int)
                )
                estudiantes = estudiantes.filter(
                    Q(id_familiar=busqueda_int)  
                )
                # Filtro las familias
                familias = Familia.objects.filter(
                    Q(id_familiar__in=adultos.values_list('id_familiar', flat=True)) |
                    Q(id_familiar__in=estudiantes.values_list('id_familiar', flat=True))
                )
            except ValueError:
                adultos = adultos.filter(
                    Q(nombre__icontains=busqueda) |
                    Q(apellido__icontains=busqueda)
                )
                estudiantes = estudiantes.filter(
                    Q(nombre__icontains=busqueda) |
                    Q(apellido__icontains=busqueda)
                )
                familias = Familia.objects.filter(
                    Q(id_familiar__in=adultos.values_list('id_familiar', flat=True)) |
                    Q(id_familiar__in=estudiantes.values_list('id_familiar', flat=True))
                )
        
        adultos2 = Adulto.objects.all() # genera un listado de los adultos para poder completar el resultado de la busqueda , en caso de quitarlo se obtenian resultados de familias incompletos
        estudiantes2 = Estudiante.objects.all() # genera un listado de los adultos para poder completar el resultado de la busqueda , en caso de quitarlo se obtenian resultados de familias incompletos
        direcciones = Direccion.objects.all()
        parentesco = Parentesco.objects.all()
        context['familias'] = familias
        context['adultos'] = adultos2
        context['parentescos'] = parentesco
        context['estudiantes'] = estudiantes2
        context['direcciones'] = direcciones

        return context
    
class RegistrarClienteView(IndexView):
    template_name='registrar_cliente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nvl_educativo = Nvl_educativo.objects.all()
        turnos = Turno.objects.all()
        parentesco = Parentesco.objects.all()
        viajes = Precio.objects.all()

        context['parentescos'] = parentesco
        context['turnos'] = turnos
        context['nvls_educativos'] = nvl_educativo
        context['viajes'] = viajes

        return context

    def post(self,request):
        if request.method == 'POST':
            v=Validaciones_C()
            
            # el programa cuenta con una limitacion en la cant. de registros por familia:
            num_adultos = 2
            num_estudiantes = 4
            num_direcciones = 2

            servicio_contratado=[] # lista de servicios contratados por los estudiantes, luego se utiliza para sacar el valor de la cuota

            datos_adultos = {} # Aqui se guardaran todos los datos ingresados en los campos pertenecientes a adultos
            adulto_completo = {} # Aca se guardaran solo los adultos que cumplan con todos los requisitos para ser registrados en la base de datos

            datos_estudiantes = {} # Aqui se guardaran todos los datos ingresados en los campos pertenecientes a adultos
            estudiante_completo = {} # Aca se guardaran solo los adultos que cumplan con todos los requisitos para ser registrados en la base de datos

            datos_direcciones = {} # Aqui se guardaran todos los datos ingresados en los campos pertenecientes a adultos
            direccion_completa = {} # Aca se guardaran solo los adultos que cumplan con todos los requisitos para ser registrados en la base de datos
 
            datos_por_completar=0 # contador para saber si hay formularios a medio compeltar o con errores
            error_descuento = None

            # a continuacion se traen los datos del html con un rangue para hacerlo la cantidad de veces estipulada anteriormente

            for i in range(1, num_adultos + 1):
                # llamo los valores de los campos del formulario del html
                nombre = request.POST.get(f'nombre-adulto-{i}')
                apellido = request.POST.get(f'apellido-adulto-{i}')
                parentesco = request.POST.get(f'opcion-adulto-{i}-parentesco')
                celular = request.POST.get(f'celular-adulto-{i}')

                # validaciones de caracteres alfabeticos, numericos y especiales
                nombre_error=v.validar_nombre(nombre)
                apellido_error=v.validar_nombre(apellido)
                parentesco_error=v.validar_parentesco(parentesco)
                celular_error=v.validar_celular_r(celular)

                # estos try los pongo para obtener el id en caso de que exista y llevarlo al front de nuevo en caso de haber algun error en el formulario
                # esto permite que no se des-seleccione la opcion
                # utilizo try para que no salte un error en caso de que venga vacio el campo

                try:
                    parentesco = Parentesco.objects.get(id=parentesco)
                except:
                    pass
                
                # en caso de que se ingrese nombre, apellido y celular se procede a validar los datos para registrarlos luego
                if nombre and apellido and celular:
                    # si todos los datos pasan las validaciones se agregan a la lista de adultos listos para realizar el registro
                    if not nombre_error and not apellido_error and not parentesco_error and not celular_error and parentesco:
                        adulto_completo[i]={
                                    'nombre': nombre,
                                    'apellido': apellido,
                                    'parentesco': parentesco.id,
                                    'celular': celular,}
                    else: 
                        # en caso de que algun campo posea algun error se sumara uno a los datos para completar, 
                        # asi no se procede con el registro hasta que se completan correctamente los campos de este adulto
                        datos_por_completar+=1
                
                datos_adultos[i] = {
                    'nombre': nombre,
                    'apellido': apellido,
                    'parentesco': parentesco,
                    'celular': celular,
                    'nombre_error': nombre_error,
                    'apellido_error': apellido_error,
                    'parentesco_error':parentesco_error,
                    'celular_error':celular_error
                } 

            for i in range(1, num_estudiantes + 1):
                nombre_estudiante = request.POST.get(f'nombre-estudiante-{i}')
                apellido_estudiante = request.POST.get(f'apellido-estudiante-{i}')
                nvl_estudiante = request.POST.get(f'opcion-estudiante-{i}-nvl-educativo')
                nvl_num_estudiante = request.POST.get(f'opcion-estudiante-{i}-nivel')
                division = request.POST.get(f'opcion-estudiante-{i}-division')
                turno = request.POST.get(f'opcion-estudiante-{i}-turno')
                viaje_estudiante = request.POST.get(f'opcion-estudiante-{i}-servicio')

                nombre_error=v.validar_nombre(nombre_estudiante)
                apellido_error=v.validar_nombre(apellido_estudiante)
                nvl_error=v.validar_nvl(nvl_estudiante)
                nvl_num_error=v.validar_nvl_num(nvl_estudiante,nvl_num_estudiante)
                division_error=v.validar_division(division)
                turno_error=v.validar_turno(turno)
                servicio_viaje_error=v.validar_servicio(viaje_estudiante)

                if viaje_estudiante !=None:
                    servicio_contratado.append(viaje_estudiante)
                
                try:
                    nvl_estudiante = Nvl_educativo.objects.get(id=nvl_estudiante)
                except:
                    pass
                try:
                    division = Division.objects.get(id=division)
                except:
                    pass
                try:
                    turno = Turno.objects.get(id=turno)
                except:
                    pass
                try:
                    viaje_estudiante = Precio.objects.get(id=viaje_estudiante)
                except:
                    pass

                if nombre_estudiante and apellido_estudiante: 
                    if nvl_estudiante and nvl_num_estudiante and division and turno and viaje_estudiante:
                        if not nombre_error and not apellido_error and not celular_error and not nvl_error and not nvl_num_error and not division_error and not turno_error and not servicio_viaje_error: 
                            estudiante_completo[i]={
                                        'nombre': nombre_estudiante,
                                        'apellido': apellido_estudiante,
                                        'nivel_educativo': nvl_estudiante.id,
                                        'nivel': nvl_num_estudiante,
                                        'division': division.id,
                                        'turno': turno.id,
                                        'servicio_viaje': viaje_estudiante.id,}
                    else:
                        datos_por_completar+=1

                datos_estudiantes[i] = {
                    'nombre': nombre_estudiante,
                    'apellido': apellido_estudiante,
                    'nivel_educativo': nvl_estudiante,
                    'nivel': nvl_num_estudiante,
                    'division': division,
                    'turno': turno,
                    'servicio_viaje': viaje_estudiante,
                    'nombre_error': nombre_error,
                    'apellido_error': apellido_error,
                    'nvl_error':nvl_error,
                    'nvl_num_error':nvl_num_error,
                    'division_error':division_error,
                    'turno_error':turno_error,
                    'servicio_viaje_error':servicio_viaje_error,
                }
                
            for i in range(1, num_direcciones + 1):
                calle = request.POST.get(f'calle-direccion-{i}')
                altura = request.POST.get(f'altura-direccion-{i}')
                piso = request.POST.get(f'piso-direccion-{i}')
                dpto = request.POST.get(f'dpto-direccion-{i}')

                calle_error=v.validar_calle(calle)
                altura_error=v.validar_altura(altura)
                piso_error=v.validar_piso(piso)
                dpto_error=v.validar_dpto(dpto)

                if calle and altura and piso and dpto:
                    if not calle_error and not altura_error and not piso_error and not dpto_error:
                        direccion_completa[i]={
                                'calle': calle,
                                'altura': altura,
                                'piso': piso,
                                'departamento': dpto,
                        }
                    else:
                        datos_por_completar+=1

                datos_direcciones[i] = {
                    'calle': calle,
                    'altura': altura,
                    'piso': piso,
                    'departamento': dpto,
                    'calle_error':calle_error,
                    'altura_error':altura_error,
                    'piso_error':piso_error,
                    'dpto_error':dpto_error,
                }

            error_x=None
            error_descuento=None
            
            descuento = request.POST.get(f'descuento') # traigo el valor de campo de descuento
            
            if descuento != '': # en caso de haber un valor se procede a valdiar que sea numerico
                validar_descuento = v.cadena_numerica(descuento)

                if validar_descuento == True: 
                    # si es numerico y hay 1 registro para adultos, estudiantes y direcciones, ademas no hay registros incompletos se procede a realizar los registros del grupo familiar
                    if adulto_completo and estudiante_completo and direccion_completa and datos_por_completar==0:           
                        r=Registro()
                        familia = Familia(estado=False)
                        familia.save()

                        familia_id = familia.id_familiar
                                
                        for datos in adulto_completo.values():
                            r.registro_adulto(familia_id,datos['nombre'].title(),datos['apellido'].title(),datos['parentesco'],datos['celular'])
                            
                        for datos in estudiante_completo.values():
                            r.registro_estudiante(familia_id,datos['nombre'].title(),datos['apellido'].title(),datos['nivel_educativo'],datos['nivel'],datos['division'],datos['turno'],datos['servicio_viaje'])

                        for datos in direccion_completa.values():                
                            r.registro_direccion(familia_id,datos['calle'].title(),datos['altura'],datos['piso'],datos['departamento'])

                        c=Cuota()
                        c.actualizar_cuota(familia_id,servicio_contratado,descuento)
                    
                        return redirect('clientes')
                    else:
                        error_x='Error, vuelva a intentarlo.*'

                else:
                    error_descuento='Ingrese solo números.*'
            else:
                    error_descuento='Ingrese un número del 0 al 100.*'

            nvl_educativo = Nvl_educativo.objects.all()
            turnos = Turno.objects.all()
            parentesco = Parentesco.objects.all()
            viajes = Precio.objects.all()
            return render(request, self.template_name, {'datos_adultos':datos_adultos,
                                                        'datos_estudiantes':datos_estudiantes,
                                                        'datos_direcciones':datos_direcciones,
                                                        'parentescos':parentesco,
                                                        'turnos':turnos,
                                                        'nvls_educativos':nvl_educativo,
                                                        'viajes':viajes,
                                                        'error_x': error_x,
                                                        'error_descuento': error_descuento,
                                                        })

class ModificarGrupoFamiliar(IndexView):
    template_name='modificar_cliente.html'

    def get(self, request, familia_id):
        # Muestro los datos registrados
        familia = Familia.objects.get(id_familiar=familia_id)
        adultos = Adulto.objects.filter(id_familiar=familia_id)
        estudiantes = Estudiante.objects.filter(id_familiar=familia_id)
        direcciones = Direccion.objects.filter(id_familiar=familia_id)
        nvl_educativo = Nvl_educativo.objects.all()
        turnos = Turno.objects.all()
        parentescos = Parentesco.objects.all()
        viajes = Precio.objects.all()

        return render(request, self.template_name, {'familia': familia,
                                                    'adultos':adultos, 
                                                    'estudiantes':estudiantes, 
                                                    'direcciones':direcciones, 
                                                    'nvls_educativos':nvl_educativo, 
                                                    'turnos':turnos, 
                                                    'parentescos':parentescos, 
                                                    'viajes':viajes})
    
    def post(self, request, familia_id):
        r=Registro()
        m=Modificar()
        e=Eliminar()
        v=Validaciones_C()
            
        num_adultos = 2
        num_estudiantes = 4
        num_direcciones = 2

        servicio_contratado=[]

        datos_adultos = {}
        adulto_completo={}
        datos_estudiantes = {}
        estudiante_completo = {}
        datos_direcciones = {}
        direccion_completa = {}
        datos_por_completar=0

        for i in range(1, num_adultos + 1):
            id_adulto = request.POST.get(f'id-adulto-{i}')
            nombre = request.POST.get(f'nombre-adulto-{i}')
            apellido = request.POST.get(f'apellido-adulto-{i}')
            parentesco = request.POST.get(f'opcion-adulto-{i}-parentesco')
            celular = request.POST.get(f'celular-adulto-{i}')

            nombre_error=v.validar_nombre(nombre)
            apellido_error=v.validar_nombre(apellido)
            parentesco_error=v.validar_parentesco(parentesco)
            celular_error=v.validar_celular_m(celular,id_adulto)

            try:
                parentesco = Parentesco.objects.get(id=parentesco)
            except:
                pass

            if nombre and apellido and celular and parentesco:
                if not nombre_error and not apellido_error and not parentesco_error and not celular_error and parentesco:
                    adulto_completo[i]={
                                'id':id_adulto,
                                'nombre': nombre,
                                'apellido': apellido,
                                'parentesco': parentesco.id,
                                'celular': celular,}
                else:
                    datos_por_completar+=1
            
            if nombre or apellido or celular or parentesco:
                datos_por_completar+=1
            
            datos_adultos[i] = {
                'id':id_adulto,
                'nombre': nombre,
                'apellido': apellido,
                'parentesco': parentesco,
                'celular': celular,
                'nombre_error': nombre_error,
                'apellido_error': apellido_error,
                'parentesco_error':parentesco_error,
                'celular_error':celular_error
            } 

        for i in range(1, num_estudiantes + 1):
            id_estudiante = request.POST.get(f'id-estudiante-{i}')
            nombre_estudiante = request.POST.get(f'nombre-estudiante-{i}')
            apellido_estudiante = request.POST.get(f'apellido-estudiante-{i}')
            nvl_estudiante = request.POST.get(f'opcion-estudiante-{i}-nvl-educativo')
            nvl_num_estudiante = request.POST.get(f'opcion-estudiante-{i}-nivel')
            division = request.POST.get(f'opcion-estudiante-{i}-division')
            turno = request.POST.get(f'opcion-estudiante-{i}-turno')
            viaje_estudiante = request.POST.get(f'opcion-estudiante-{i}-servicio')

            nombre_error=v.validar_nombre(nombre_estudiante)
            apellido_error=v.validar_nombre(apellido_estudiante)
            nvl_error=v.validar_nvl(nvl_estudiante)
            nvl_num_error=v.validar_nvl_num(nvl_estudiante,nvl_num_estudiante)
            division_error=v.validar_division(division)
            turno_error=v.validar_turno(turno)
            servicio_viaje_error=v.validar_servicio(viaje_estudiante)

            if viaje_estudiante !=None:
                    servicio_contratado.append(viaje_estudiante)
                
            try:
                nvl_estudiante = Nvl_educativo.objects.get(id=nvl_estudiante)
            except:
                pass
            try:
                division = Division.objects.get(id=division)
            except:
                pass
            try:
                turno = Turno.objects.get(id=turno)
            except:
                pass
            try:
                viaje_estudiante = Precio.objects.get(id=viaje_estudiante)
            except:
                pass

            if nombre_estudiante and apellido_estudiante: 
                if nvl_estudiante and nvl_num_estudiante and division and turno and viaje_estudiante:
                    if not nombre_error and not apellido_error and not nvl_error and not nvl_num_error and not division_error and not turno_error and not servicio_viaje_error:     
                        estudiante_completo[i]={
                                    'id':id_estudiante,
                                    'nombre': nombre_estudiante,
                                    'apellido': apellido_estudiante,
                                    'nivel_educativo': nvl_estudiante.id,
                                    'nivel': nvl_num_estudiante,
                                    'division': division.id,
                                    'turno': turno.id,
                                    'servicio_viaje': viaje_estudiante.id,}
                else:
                    datos_por_completar+=1
            
            if nombre_estudiante or apellido_estudiante or nvl_estudiante or nvl_num_estudiante or division or turno or viaje_estudiante:
                datos_por_completar+=1

            datos_estudiantes[i] = {
                'id':id_estudiante,
                'nombre': nombre_estudiante,
                'apellido': apellido_estudiante,
                'nivel_educativo': nvl_estudiante,
                'nivel': nvl_num_estudiante,
                'division': division,
                'turno': turno,
                'servicio_viaje': viaje_estudiante,
                'nombre_error': nombre_error,
                'apellido_error': apellido_error,
                'nvl_error':nvl_error,
                'nvl_num_error':nvl_num_error,
                'division_error':division_error,
                'turno_error':turno_error,
                'servicio_viaje_error':servicio_viaje_error,
            }
            
        for i in range(1, num_direcciones + 1):
            id_direccion = request.POST.get(f'id-direccion-{i}')
            calle = request.POST.get(f'calle-direccion-{i}')
            altura = request.POST.get(f'altura-direccion-{i}')
            piso = request.POST.get(f'piso-direccion-{i}')
            dpto = request.POST.get(f'dpto-direccion-{i}')

            calle_error=v.validar_calle(calle)
            altura_error=v.validar_altura(altura)
            piso_error=v.validar_piso(piso)
            dpto_error=v.validar_dpto(dpto)

            if calle and altura and piso and dpto:
                if not calle_error and not altura_error and not piso_error and not dpto_error:
                    direccion_completa[i]={
                            'id':id_direccion,
                            'calle': calle,
                            'altura': altura,
                            'piso': piso,
                            'departamento': dpto,
                    }
                else:
                    datos_por_completar+=1
            
            if calle or altura or piso or dpto:
                datos_por_completar+=1

            datos_direcciones[i] = {
                'id':id_direccion,
                'calle': calle,
                'altura': altura,
                'piso': piso,
                'departamento': dpto,
                'calle_error':calle_error,
                'altura_error':altura_error,
                'piso_error':piso_error,
                'dpto_error':dpto_error,
            }

        error_x=None
        error_descuento=None
        
        descuento = request.POST.get(f'descuento') # traigo el valor de campo de descuento
        
        if descuento != '': # en caso de haber un valor se procede a valdiar que sea numerico
            validar_descuento = v.cadena_numerica(descuento)

            if validar_descuento == True: 
                # si es numerico y hay 1 registro para adultos, estudiantes y direcciones, ademas no hay registros incompletos se procede a realizar los registros del grupo familiar
                if adulto_completo and estudiante_completo and direccion_completa and datos_por_completar==0:
                    descuento = request.POST.get(f'descuento')
                    print(adulto_completo)
                    print('-----------------')
                    print(datos_adultos)
                    for datos in adulto_completo.values():
                        if datos['id'] == '' or datos['id'] == None:
                            # Si no tiene id pero recibo datos realizo un registro
                            r.registro_adulto(familia_id,datos['nombre'].title(),datos['apellido'].title(),datos['parentesco'],datos['celular'])

                        if datos['id'] != '' and datos['id'] != None:
                            if datos['nombre'] == '' and datos['apellido'] == '':
                                # Si tenia id y vienen los campos vacios elimino al integrante
                                e.eliminar_adulto(datos['id'])
                            else:
                                # Si tiene id y viene con contenido actualizo la tabla
                                m.modificar_adulto(datos['id'],datos['nombre'].title(),datos['apellido'].title(),datos['parentesco'],datos['celular'])

                    if datos_adultos:
                        for i in datos_adultos.values():
                                if i['id'] != '' and i['nombre']=='':
                                    e.eliminar_adulto(i['id'])
                                if i['id'] != None and i['nombre']==None:
                                    e.eliminar_adulto(i['id'])

                    for datos in estudiante_completo.values():
                        if datos['id'] == '' or datos['id'] == None:
                            # Si no tiene id pero recibo datos realizo un registro
                            r.registro_estudiante(familia_id,datos['nombre'].title(),datos['apellido'].title(),datos['nivel_educativo'],datos['nivel'],datos['division'],datos['turno'],datos['servicio_viaje'])

                        elif datos['id'] != '' and datos['id'] != None:
                            if datos['nombre'] == '' and datos['apellido'] == '':
                                # Si tenia id y vienen los campos vacios elimino al integrante
                                e.eliminar_estudiante(datos['id'])
                            else:
                                # Si tiene id y viene con contenido actualizo la tabla
                                m.modificar_estudiante(datos['id'],datos['nombre'].title(),datos['apellido'].title(),datos['nivel_educativo'],datos['nivel'],datos['division'],datos['turno'],datos['servicio_viaje'])

                    if datos_estudiantes:
                        for i in datos_estudiantes.values():
                                if i['id'] != '' and i['nombre']=='':
                                    e.eliminar_estudiante(i['id'])
                                if i['id'] != None and i['nombre']==None:
                                    e.eliminar_estudiante(i['id'])
                                
                    for datos in datos_direcciones.values():
                        if datos['id'] == '' or datos['id'] == None:
                            # Si no tiene id pero recibo datos realizo un registro
                            r.registro_direccion(familia_id,datos['calle'].title(),datos['altura'],datos['piso'],datos['departamento'])
                        
                        elif datos['id'] != '' or datos['id'] != None:
                            if datos['calle'] == '' and datos['altura'] == '' and datos['piso'] == '' and datos['departamento'] == '':
                                # Si tenía id y vienen los campos vacíos elimino al integrante
                                e.eliminar_direccion(datos['id'])
                            else:
                                # Si tiene id y viene con contenido actualizo la tabla
                                m.modificar_direccion(datos['id'],datos['calle'].title(),datos['altura'],datos['piso'],datos['departamento'])

                    if datos_direcciones:
                        for i in datos_direcciones.values():
                                if i['id'] != '' and i['calle']=='':
                                    e.eliminar_direccion(i['id'])
                                if i['id'] != None and i['calle']==None:
                                    e.eliminar_direccion(i['id'])

                    c=Cuota()
                    c.actualizar_cuota(familia_id,servicio_contratado,descuento)

                    return redirect('clientes')
        
                else:
                    error_x='Error, vuelva a intentarlo.*'

            else:
                error_descuento='Ingrese solo números.*'
        else:
            error_descuento='Ingrese un número del 0 al 100.*'

        

    
        nvl_educativo = Nvl_educativo.objects.all()
        turnos = Turno.objects.all()
        parentesco = Parentesco.objects.all()
        viajes = Precio.objects.all()
        familia = Familia.objects.get(id_familiar=familia_id)
        adultos = Adulto.objects.filter(id_familiar=familia_id)
        estudiantes = Estudiante.objects.filter(id_familiar=familia_id)
        direcciones = Direccion.objects.filter(id_familiar=familia_id)

        return render(request, self.template_name, {'datos_adultos':datos_adultos,
                                                    'datos_estudiantes':datos_estudiantes,
                                                    'datos_direcciones':datos_direcciones,
                                                    'parentescos':parentesco,
                                                    'turnos':turnos,
                                                    'nvls_educativos':nvl_educativo,
                                                    'viajes':viajes,
                                                    'familia':familia,
                                                    'adultos':adultos, 
                                                    'estudiantes':estudiantes, 
                                                    'direcciones':direcciones,
                                                    'error_x': error_x,
                                                    'error_descuento': error_descuento,
                                                    })
    
class EliminarGrupoFamiliarView(IndexView):
    template_name = 'eliminar_cliente.html'

    def get(self, request, familia_id):
        familia = Familia.objects.get(id_familiar=familia_id)
        adultos = Adulto.objects.filter(id_familiar=familia_id)
        estudiantes = Estudiante.objects.filter(id_familiar=familia_id)
        direcciones = Direccion.objects.filter(id_familiar=familia_id)
        viajes = Precio.objects.all()

        return render(request, self.template_name, {'familia': familia,'adultos':adultos, 'estudiantes':estudiantes, 'direcciones':direcciones, 'viajes':viajes})

    def post(self, request, familia_id):
        # Busca la familia
        familia = Familia.objects.get(id_familiar=familia_id)
        adultos = Adulto.objects.filter(id_familiar=familia_id)
        estudiantes = Estudiante.objects.filter(id_familiar=familia_id)
        direcciones = Direccion.objects.filter(id_familiar=familia_id)

        for adulto in adultos:
            adulto.delete()

        for estudiante in estudiantes:
            estudiante.delete()
        
        for direccion in direcciones:
            direccion.delete()
            
        familia.delete()

        return redirect('clientes')

class CargarDivisionesView(View):
    
    def get(self, request, *args, **kwargs):
        nivel_educativo_id = self.request.GET.get('nivel_educativo')

        # Filtra las divisiones basadas en el nivel educativo seleccionado
        divisiones = Division.objects.filter(id_nvl_educativo=nivel_educativo_id)

        # Crea una lista de diccionarios con las divisiones
        divisiones_list = [{'id': division.id, 'division': division.division} for division in divisiones]

        # Devuelve las divisiones como una respuesta JSON
        data = {'divisiones': divisiones_list}
        return JsonResponse(data)
    