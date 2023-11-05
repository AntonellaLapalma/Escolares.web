from django.shortcuts import render, redirect, get_object_or_404
from apps.home.views import IndexView
from apps.vehiculos.models import Vehiculo
from apps.empleados.models import *
from apps.recorridos.models import *
from .funciones_vehiculos import *


class VehiculosView(IndexView):
    template_name='mostrar_vehiculos.html'

    def get(self, request, *args, **kwargs):
        # En caso de que no se haya iniciado sesion redirige a login
        if not request.user.is_authenticated:
            return redirect('login')

        # Obtengo el valor del parametro 'estado' en la URL
        chofer = self.kwargs.get('estado')

        # Si el parametro 'estado' esta presente filtro los vehiculos
        if chofer == 'activo':
            vehiculos = Vehiculo.objects.exclude(chofer=None)
        elif chofer == 'inactivo':
            vehiculos = Vehiculo.objects.filter(chofer=None)
        else:
            # Si no obtengo todos los vehiculos
            vehiculos = Vehiculo.objects.all()

        # Obtengo el valor del parametro 'busqueda' en la URL
        busqueda = self.request.GET.get('busqueda', '')
        
        if busqueda:

            vehiculos = vehiculos.filter(
                Q(patente__icontains=busqueda)
                )

        for vehiculo in vehiculos:
            viajes_distintos_l = Lunes.objects.filter(vehiculo=vehiculo).values('viaje__turno', 'viaje__tipo').distinct()
            vehiculo.l = viajes_distintos_l.count()
            viajes_distintos_m = Martes.objects.filter(vehiculo=vehiculo.id).values('viaje__turno', 'viaje__tipo').distinct()
            vehiculo.m = viajes_distintos_m.count()
            viajes_distintos_x = Miercoles.objects.filter(vehiculo=vehiculo.id).values('viaje__turno', 'viaje__tipo').distinct()
            vehiculo.x = viajes_distintos_x.count()
            viajes_distintos_j = Jueves.objects.filter(vehiculo=vehiculo.id).values('viaje__turno', 'viaje__tipo').distinct()
            vehiculo.j = viajes_distintos_j.count()
            viajes_distintos_v = Viernes.objects.filter(vehiculo=vehiculo.id).values('viaje__turno', 'viaje__tipo').distinct()
            vehiculo.v = viajes_distintos_v.count()
        return render(request, self.template_name, {'vehiculos':vehiculos})
    
class RegistrarVehiculoView(VehiculosView):
    template_name='registrar_vehiculo.html'

    def get(self, request, *args, **kwargs):
        # En caso de que no se haya iniciado sesion redirige a login
        if not request.user.is_authenticated:
            return redirect('login')

        td=Traer_Datos()
        # Traigo los empleados para luego listarlos en el html
        empleados_sin_asignar = td.empleados_libres()

        empleados = empleados_sin_asignar
        return render(request, self.template_name, {'empleados':empleados})

    def post(self,request):
        error_x=None
        if request.method == 'POST':

            # Trae la informacion del input segun el nombre asignado
            patente = request.POST.get('patente_vehiculo').lower()
            asientos = request.POST.get('asientos_vehiculo')
            chofer_id = request.POST.get('opcion_chofer')
            celador_id = request.POST.get('opcion_celador')

            # Instancias de Empleado a partir de los id
            if chofer_id != 'Ninguno' and chofer_id.isdigit():
                chofer = get_object_or_404(Empleado, id=chofer_id)
            elif chofer_id == 'Ninguno':
                chofer=None
            else:
                error_x = 'Error, vuelva a intentarlo.*'

            if celador_id != 'Ninguno' and celador_id.isdigit():
                celador = get_object_or_404(Empleado, id=celador_id)
            elif celador_id == 'Ninguno':
                celador=None
            else:
                error_x = 'Error, vuelva a intentarlo.*'

            v = Validar_Ingresos_v()

            patente_error = v.validar_patente_r(patente)
            asientos_error = v.validar_asientos(asientos)
            chofer_val = v.validar_existencia_chofer(chofer_id)
            celador_val = v.validar_existencia_celador(celador_id)
            
            
            if not patente_error and not asientos_error and chofer_id == 'Ninguno' and celador_id == 'Ninguno':
                vehiculo = Vehiculo(patente=patente, cant_asientos=asientos, chofer=chofer, celador=celador)
                vehiculo.save()
                return redirect('vehiculos')
            elif not patente_error and not asientos_error and chofer_val and celador_val:
                vehiculo = Vehiculo(patente=patente, cant_asientos=asientos, chofer=chofer, celador=celador)
                vehiculo.save()
                return redirect('vehiculos')
            
            td=Traer_Datos()
            # Traigo los empleados para luego listarlos en el html
            empleados_sin_asignar = td.empleados_libres()

        return render(request, self.template_name, {'patente_error': patente_error,
                                                    'asientos_error': asientos_error,
                                                    'error_x': error_x,
                                                    'empleados':empleados_sin_asignar
                                                    })
    
class ModificarVehiculoView(VehiculosView):
    template_name='modificar_vehiculo.html'

    def get(self, request, *args, **kwargs):
        # En caso de que no se haya iniciado sesion redirige a login
        if not request.user.is_authenticated:
            return redirect('login')

        vehiculo = None
        empleados_sin_asignar = None

        vehiculo_id = kwargs.get('vehiculo_id')
        if vehiculo_id:
            vehiculo = Vehiculo.objects.get(id=vehiculo_id)
            td = Traer_Datos()
            empleados_sin_asignar = td.empleados_libres()

        return render(request, self.template_name, {'vehiculo': vehiculo, 
                                                    'empleados': empleados_sin_asignar})
        
    def post(self, request, vehiculo_id):
        error_x=None
        vehiculo = Vehiculo.objects.get(id=vehiculo_id)

        # Actualizo los datos del vehiculo con los valores enviados en el formulario
        patenteN = request.POST.get('patente_vehiculo').lower()
        asientos = request.POST.get('asientos_vehiculo')
        chofer_id = request.POST.get('opcion_chofer')
        celador_id = request.POST.get('opcion_celador')

        # Instancias de Empleado a partir de los id
        if chofer_id != 'Ninguno':
            chofer = get_object_or_404(Empleado, id=chofer_id)
        elif chofer_id == 'Ninguno':
            chofer=None
        else:
            error_x = 'Error, vuelva a intentarlo.*'
            
        if celador_id != 'Ninguno':
            celador = get_object_or_404(Empleado, id=celador_id)
        elif celador_id == 'Ninguno':
            celador=None
        else:
            error_x = 'Error, vuelva a intentarlo.*'

        v = Validar_Ingresos_v()

        patente_error = v.validar_patente_m(patenteN,vehiculo.id)
        asientos_error = v.validar_asientos(asientos)
        chofer_val = v.validar_existencia_chofer(chofer_id)
        celador_val = v.validar_existencia_celador(celador_id)
        print(chofer_val,celador_val)
        
        if not patente_error and not asientos_error and chofer_id == 'Ninguno' and celador_id == 'Ninguno':
            vehiculo.patente = patenteN
            vehiculo.cant_asientos = asientos
            vehiculo.chofer = chofer
            vehiculo.celador = celador
            vehiculo.save()
            return redirect('vehiculos')
        if not patente_error and not asientos_error:
            vehiculo.patente = patenteN
            vehiculo.cant_asientos = asientos
            if chofer_val:
                vehiculo.chofer = Empleado.objects.get(id=chofer_id)
            if celador_val:
                vehiculo.celador = Empleado.objects.get(id=celador_id)
            vehiculo.save()
            return redirect('vehiculos')
        
        td=Traer_Datos()
        # Traigo los empleados para luego listarlos en el html
        empleados_sin_asignar = td.empleados_libres()

        return render(request, self.template_name, {'patente_error': patente_error,
                                                    'asientos_error': asientos_error,
                                                    'error_x': error_x,
                                                    'empleados':empleados_sin_asignar,
                                                    'vehiculo':vehiculo
                                                    })
    
class EliminarVehiculoView(VehiculosView):
    template_name='eliminar_vehiculo.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        vehiculo = None
        vehiculo_id = kwargs.get('vehiculo_id')
        
        if vehiculo_id:
            vehiculo = Vehiculo.objects.get(id=vehiculo_id)

        return render(request, self.template_name, {'vehiculo': vehiculo})

    
    def post(self, *args, **kwargs):
        vehiculo = None
        vehiculo_id = kwargs.get('vehiculo_id')
        
        if vehiculo_id:
            vehiculo = Vehiculo.objects.get(id=vehiculo_id)
        vehiculo.delete()

        return redirect('vehiculos')
