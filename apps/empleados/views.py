from django.shortcuts import render, redirect, get_object_or_404
from apps.home.views import IndexView
from apps.empleados.models import *
from apps.vehiculos.models import Vehiculo
from django.db.models import Q
from .funciones_empleados import *

class EmpleadosView(IndexView):
    template_name = 'mostrar_empleados.html'

    def get(self, request, *args, **kwargs):
        # En caso de que no se haya iniciado sesion redirige a login
        if not request.user.is_authenticated:
            return redirect('login')

        # Obtengo el valor del 'estado' en la URL
        puesto = self.kwargs.get('estado')

        # Si esta presente, filtro los empleados
        if puesto == 'activo':
            empleados = Empleado.objects.exclude(puesto=None)
        elif puesto == 'inactivo':
            empleados = Empleado.objects.filter(puesto=None)
        else:
            # Si no obtengo todos los empleados
            empleados = Empleado.objects.all()

        # Obtengo el valor de 'busqueda' en la URL
        busqueda = self.request.GET.get('busqueda', '')

        if busqueda:
            try:
                busqueda_int = int(busqueda)

                # Filtra empleados
                empleados = empleados.filter(
                    Q(id=busqueda_int) |
                    Q(celular=busqueda_int)
                )
            except ValueError:
                empleados = empleados.filter(
                    Q(nombre__icontains=busqueda) |
                    Q(apellido__icontains=busqueda)
                )

        # Busco los vehiculos vinculados con los empleados
        vehiculos = Vehiculo.objects.all()

        for empleado in empleados:
            empleado.vehiculo_asignado = "Sin asignar"

            for vehiculo in vehiculos:
                if vehiculo.chofer and empleado.id == vehiculo.chofer.id:
                    empleado.vehiculo_asignado = vehiculo
                    viajes_distintos_l = Lunes.objects.filter(vehiculo=vehiculo.id).values('viaje__turno', 'viaje__tipo').distinct()
                    empleado.l = viajes_distintos_l.count()
                    viajes_distintos_m = Martes.objects.filter(vehiculo=vehiculo.id).values('viaje__turno', 'viaje__tipo').distinct()
                    empleado.m = viajes_distintos_m.count()
                    viajes_distintos_x = Miercoles.objects.filter(vehiculo=vehiculo.id).values('viaje__turno', 'viaje__tipo').distinct()
                    empleado.x = viajes_distintos_x.count()
                    viajes_distintos_j = Jueves.objects.filter(vehiculo=vehiculo.id).values('viaje__turno', 'viaje__tipo').distinct()
                    empleado.j = viajes_distintos_j.count()
                    viajes_distintos_v = Viernes.objects.filter(vehiculo=vehiculo.id).values('viaje__turno', 'viaje__tipo').distinct()
                    empleado.v = viajes_distintos_v.count()
                    break
                elif vehiculo.celador and empleado.id == vehiculo.celador.id:
                    empleado.vehiculo_asignado = vehiculo
                    viajes_distintos_l = Lunes.objects.filter(vehiculo=vehiculo.id).values('viaje__turno', 'viaje__tipo').distinct()
                    empleado.l = viajes_distintos_l.count() 
                    viajes_distintos_m = Martes.objects.filter(vehiculo=vehiculo.id).values('viaje__turno', 'viaje__tipo').distinct()
                    empleado.m = viajes_distintos_m.count()         
                    viajes_distintos_x = Miercoles.objects.filter(vehiculo=vehiculo.id).values('viaje__turno', 'viaje__tipo').distinct()
                    empleado.x = viajes_distintos_x.count()
                    viajes_distintos_j = Jueves.objects.filter(vehiculo=vehiculo.id).values('viaje__turno', 'viaje__tipo').distinct()
                    empleado.j = viajes_distintos_j.count()
                    viajes_distintos_v = Viernes.objects.filter(vehiculo=vehiculo.id).values('viaje__turno', 'viaje__tipo').distinct()
                    empleado.v = viajes_distintos_v.count()
                    break
                
        return render(request, self.template_name,{'empleados':empleados})

class RegistrarEmpleadoView(IndexView):
    template_name='registrar_empleado.html'

    def get(self, request, *args, **kwargs):
        # En caso de que no se haya iniciado sesion redirige a login
        if not request.user.is_authenticated:
            return redirect('login')

        puestos = Puesto.objects.all()
        return render(request, self.template_name, {'puestos':puestos})
    
    def post(self, request):
        error_x=None
        nombre_error = None
        apellido_error = None
        celular_error = None
        nombre = ""
        apellido = ""
        celular = ""
        
        if request.method == 'POST':
            puestos = Puesto.objects.all()

            # Formulario
            nombre = request.POST.get('nombre_empleado')
            apellido = request.POST.get('apellido_empleado')
            celular = request.POST.get('cel_empleado')
            puesto_id = request.POST.get('opcion_tarea')

            # Obtengo el objeto de Puesto seleccionado
            if puesto_id == 'Ninguno' or puesto_id == 'Chofer' or puesto_id == 'Celador':
                if puesto_id != 'Ninguno':
                    puesto = get_object_or_404(Puesto, puesto=puesto_id) # en caso de no encontrarlo mostrara una pagina de rror 404
                else:
                    puesto=None
            else:
                error_x='Error, vuelva a intentarlo.*'

            v = Validar_Ingresos()

            nombre_error = v.validar_nombre_empleado(nombre)
            apellido_error = v.validar_apellido_empleado(apellido)
            celular_error = v.validar_celular_empleado(celular)

            if not nombre_error and not apellido_error and not celular_error:
                if puesto_id == 'Ninguno' or puesto_id == 'Chofer' or puesto_id == 'Celador':
                    # Creo el objeto de Empleado
                    empleado = Empleado(nombre=nombre, apellido=apellido, celular=celular, puesto=puesto)
                    empleado.save()
                    return redirect('empleados')
            
        return render(request, self.template_name, {'nombre_error': nombre_error,
                                                    'apellido_error': apellido_error,
                                                    'celular_error': celular_error,
                                                    'nombre': nombre,
                                                    'apellido': apellido,
                                                    'celular': celular,
                                                    'error_x': error_x,
                                                    'puestos':puestos
                                                    })

class ModificarEmpleadoView(IndexView):
    template_name='modificar_empleado.html'

    def get(self, request, empleado_id):
        if not request.user.is_authenticated:
            return redirect('login')
        
        empleado = Empleado.objects.get(id=empleado_id)
        puestos = Puesto.objects.all()
        return render(request, self.template_name, {'empleado': empleado,
                                                    'puestos':puestos})
 
    def post(self, request, empleado_id):
        nombre = ""
        apellido = ""
        celular = ""
        puestos = Puesto.objects.all()
        id = self.kwargs.get('empleado_id')
        empleado = Empleado.objects.get(id=id)

        nombre = request.POST.get('nombre_empleado')
        apellido = request.POST.get('apellido_empleado')
        celular = request.POST.get('cel_empleado')
        puesto_id = request.POST.get('opcion_tarea')
        
        v = Validar_Ingresos()

        nombre_error = v.validar_nombre_empleado(nombre)
        apellido_error = v.validar_apellido_empleado(apellido)
        celular_error = v.validar_celular_modificacion(celular,empleado.id)

        if not nombre_error and not apellido_error and not celular_error:
            if puesto_id == 'Ninguno' or puesto_id == 'Chofer' or puesto_id == 'Celador':
                empleado = Empleado.objects.get(id=empleado_id)
                # Creo el objeto de Empleado
                # Actualizo los datos del empleado con los del formulario
                empleado.nombre = request.POST.get('nombre_empleado')
                empleado.apellido = request.POST.get('apellido_empleado')
                empleado.celular = request.POST.get('cel_empleado')
                puesto_id = request.POST.get('opcion_tarea')

                if empleado.puesto:
                    # Verifica si el empleado estaba asignado en algun vehiculo
                    vehiculo_chofer = Vehiculo.objects.filter(chofer=empleado)
                    vehiculo_celador = Vehiculo.objects.filter(celador=empleado)

                    # Si el empleado estaba asignado se lo desvincula
                    if vehiculo_chofer.exists() or vehiculo_celador.exists():
                        for vehiculo in vehiculo_chofer:
                            vehiculo.chofer = None
                            vehiculo.save()
                        for vehiculo in vehiculo_celador:
                            vehiculo.celador = None
                            vehiculo.save()

                # Luego asigno el nuevo puesto
                if puesto_id == 'Ninguno' or puesto_id == 'Chofer' or puesto_id == 'Celador':
                    if puesto_id != 'Ninguno':
                        empleado.puesto = get_object_or_404(Puesto, puesto=puesto_id)
                    else:
                        empleado.puesto = None
                empleado.save()
                return redirect('empleados')

        return render(request, self.template_name, {'nombre_error': nombre_error,
                                                    'apellido_error': apellido_error,
                                                    'celular_error': celular_error,
                                                    'nombre': nombre,
                                                    'apellido': apellido,
                                                    'celular': celular,
                                                    'puestos':puestos,
                                                    'empleado': empleado
                                                    })
    
class EliminarEmpleadoView(IndexView):
    template_name = 'eliminar_empleado.html'

    def get(self, request, empleado_id):
        if not request.user.is_authenticated:
            return redirect('login')
        
        empleado = Empleado.objects.get(id=empleado_id)
        return render(request, self.template_name, {'empleado': empleado})

    def post(self, request, empleado_id):
        empleado = Empleado.objects.get(id=empleado_id)

        # Elimina el empleado
        empleado.delete()

        return redirect('empleados')
