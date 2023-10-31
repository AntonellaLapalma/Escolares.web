from django.shortcuts import render, redirect
from django.views import View
from apps.clientes.estudiantes.models import *
from apps.vehiculos.models import Vehiculo
from apps.recorridos.models import *
from apps.home.views import IndexView
from django.http import JsonResponse
from .funciones_recorridos import *

class RecorridosView(IndexView):
    template_name='mostrar_recorridos.html'

    def get(self, request, *args, **kwargs):
        # En caso de que no se haya iniciado sesion redirige a login
        if not request.user.is_authenticated:
            return redirect('login')

        # Llamo al metodo get_context_data y paso los resultados
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        vehiculo_seleccionado = self.kwargs.get('vehiculo_id')
        dia = self.kwargs.get('dia').lower()

        vehiculo = Vehiculo.objects.get(id=vehiculo_seleccionado)

        l=FuncionesLunes()
        m=FuncionesMartes()
        x=FuncionesMiercoles()
        j=FuncionesJueves()
        v=FuncionesViernes()
        
        if dia == 'lunes':
            resultado = Lunes.objects.filter(vehiculo=vehiculo.id)
            mi_estudiantes_sin_recorrido=l.filtrar_lunes(vehiculo_seleccionado,'Mañana','Ingreso')
            mds_estudiantes_sin_recorrido=l.filtrar_lunes(vehiculo_seleccionado,'Medio dia','Salida')
            mdi_estudiantes_sin_recorrido=l.filtrar_lunes(vehiculo_seleccionado,'Medio dia','Ingreso')
            ts_estudiantes_sin_recorrido=l.filtrar_lunes(vehiculo_seleccionado,'Tarde','Salida')

            # Establecer tope de pasajeros
            mi_lugar_disponible=l.lugares_disponibles_l(vehiculo_seleccionado,'Mañana','Ingreso')
            mds_lugar_disponible=l.lugares_disponibles_l(vehiculo_seleccionado,'Medio dia','Salida')
            mdi_lugar_disponible=l.lugares_disponibles_l(vehiculo_seleccionado,'Medio dia','Ingreso')
            ts_lugar_disponible=l.lugares_disponibles_l(vehiculo_seleccionado,'Tarde','Salida')
            
        if dia == 'martes':
            resultado = Martes.objects.filter(vehiculo=vehiculo.id)
            mi_estudiantes_sin_recorrido=m.filtrar_martes(vehiculo_seleccionado,'Mañana','Ingreso')
            mds_estudiantes_sin_recorrido=m.filtrar_martes(vehiculo_seleccionado,'Medio dia','Salida')
            mdi_estudiantes_sin_recorrido=m.filtrar_martes(vehiculo_seleccionado,'Medio dia','Ingreso')
            ts_estudiantes_sin_recorrido=m.filtrar_martes(vehiculo_seleccionado,'Tarde','Salida')
            
            mi_lugar_disponible=m.lugares_disponibles_m(vehiculo_seleccionado,'Mañana','Ingreso')
            mds_lugar_disponible=m.lugares_disponibles_m(vehiculo_seleccionado,'Medio dia','Salida')
            mdi_lugar_disponible=m.lugares_disponibles_m(vehiculo_seleccionado,'Medio dia','Ingreso')
            ts_lugar_disponible=m.lugares_disponibles_m(vehiculo_seleccionado,'Tarde','Salida')
            
        if dia == 'miercoles':
            resultado = Miercoles.objects.filter(vehiculo=vehiculo.id)
            mi_estudiantes_sin_recorrido=x.filtrar_miercoles(vehiculo_seleccionado,'Mañana','Ingreso')
            mds_estudiantes_sin_recorrido=x.filtrar_miercoles(vehiculo_seleccionado,'Medio dia','Salida')
            mdi_estudiantes_sin_recorrido=x.filtrar_miercoles(vehiculo_seleccionado,'Medio dia','Ingreso')
            ts_estudiantes_sin_recorrido=x.filtrar_miercoles(vehiculo_seleccionado,'Tarde','Salida')
            
            mi_lugar_disponible=x.lugares_disponibles_x(vehiculo_seleccionado,'Mañana','Ingreso')
            mds_lugar_disponible=x.lugares_disponibles_x(vehiculo_seleccionado,'Medio dia','Salida')
            mdi_lugar_disponible=x.lugares_disponibles_x(vehiculo_seleccionado,'Medio dia','Ingreso')
            ts_lugar_disponible=x.lugares_disponibles_x(vehiculo_seleccionado,'Tarde','Salida')
            
        if dia == 'jueves':
            resultado = Jueves.objects.filter(vehiculo=vehiculo.id)
            mi_estudiantes_sin_recorrido=j.filtrar_jueves(vehiculo_seleccionado,'Mañana','Ingreso')
            mds_estudiantes_sin_recorrido=j.filtrar_jueves(vehiculo_seleccionado,'Medio dia','Salida')
            mdi_estudiantes_sin_recorrido=j.filtrar_jueves(vehiculo_seleccionado,'Medio dia','Ingreso')
            ts_estudiantes_sin_recorrido=j.filtrar_jueves(vehiculo_seleccionado,'Tarde','Salida')
        
            mi_lugar_disponible=j.lugares_disponibles_j(vehiculo_seleccionado,'Mañana','Ingreso')
            mds_lugar_disponible=j.lugares_disponibles_j(vehiculo_seleccionado,'Medio dia','Salida')
            mdi_lugar_disponible=j.lugares_disponibles_j(vehiculo_seleccionado,'Medio dia','Ingreso')
            ts_lugar_disponible=j.lugares_disponibles_j(vehiculo_seleccionado,'Tarde','Salida')
            
        if dia == 'viernes':
            resultado = Viernes.objects.filter(vehiculo=vehiculo.id)
            mi_estudiantes_sin_recorrido=v.filtrar_viernes(vehiculo_seleccionado,'Mañana','Ingreso')
            mds_estudiantes_sin_recorrido=v.filtrar_viernes(vehiculo_seleccionado,'Medio dia','Salida')
            mdi_estudiantes_sin_recorrido=v.filtrar_viernes(vehiculo_seleccionado,'Medio dia','Ingreso')
            ts_estudiantes_sin_recorrido=v.filtrar_viernes(vehiculo_seleccionado,'Tarde','Salida')
            
            mi_lugar_disponible=v.lugares_disponibles_v(vehiculo_seleccionado,'Mañana','Ingreso')
            mds_lugar_disponible=v.lugares_disponibles_v(vehiculo_seleccionado,'Medio dia','Salida')
            mdi_lugar_disponible=v.lugares_disponibles_v(vehiculo_seleccionado,'Medio dia','Ingreso')
            ts_lugar_disponible=v.lugares_disponibles_v(vehiculo_seleccionado,'Tarde','Salida')
            
        if vehiculo.chofer == None:
            context['celular'] = 0
        else:
            context['celular'] = vehiculo.chofer.celular 

        context['dia'] = dia
        context['resultados'] = resultado 
        context['vehiculo'] = vehiculo
        context['estudiantes1'] = mi_estudiantes_sin_recorrido
        context['estudiantes2'] = mds_estudiantes_sin_recorrido
        context['estudiantes3'] = mdi_estudiantes_sin_recorrido
        context['estudiantes4'] = ts_estudiantes_sin_recorrido
        context['mi_lugar_disponible']=mi_lugar_disponible
        context['mds_lugar_disponible']=mds_lugar_disponible
        context['mdi_lugar_disponible']=mdi_lugar_disponible
        context['ts_lugar_disponible']=ts_lugar_disponible
        
        return context
    
    def post(self,request, vehiculo_id, dia):
        if request.method == 'POST':
            turno = request.POST.get('turno')

            if turno == 'ingreso-m':
                estudiante = request.POST.get('agregar-alumno-m')
                direccion = request.POST.get('agregar-direccion-m')
                turno = 'Mañana'
                tipo = 'Ingreso'
            
            if turno == 'salida-md':
                estudiante = request.POST.get('agregar-alumno-md')
                direccion = request.POST.get('agregar-direccion-md')
                turno = 'Medio dia'
                tipo = 'Salida'

            if turno == 'ingreso-md':
                estudiante = request.POST.get('agregar-alumno-md-i')
                direccion = request.POST.get('agregar-direccion-md-i')
                turno = 'Medio dia'
                tipo = 'Ingreso'

            if turno == 'salida-t':
                estudiante = request.POST.get('agregar-alumno-t')
                direccion = request.POST.get('agregar-direccion-t')  
                turno = 'Tarde'
                tipo = 'Salida'          
            
            vehiculo = Vehiculo.objects.get(id=vehiculo_id)
            estudiante = Estudiante.objects.get(id=estudiante)
            direccion = Direccion.objects.get(id=direccion)
            viaje = Viaje.objects.get(turno=turno, tipo=tipo)
            
            l=FuncionesLunes()
            m=FuncionesMartes()
            x=FuncionesMiercoles()
            j=FuncionesJueves()
            v=FuncionesViernes()

            if dia == 'lunes':
                mi_estudiantes_sin_recorrido=l.lugares_disponibles_l(vehiculo_id,turno,tipo)
                if mi_estudiantes_sin_recorrido == True:
                    actualizar = Lunes(vehiculo=vehiculo, estudiante=estudiante, direccion=direccion,  viaje=viaje)
                pass

            if dia == 'martes':
                mi_estudiantes_sin_recorrido=m.lugares_disponibles_m(vehiculo_id,turno,tipo)
                if mi_estudiantes_sin_recorrido == True:
                    actualizar = Martes(vehiculo=vehiculo, estudiante=estudiante, direccion=direccion,  viaje=viaje)

            if dia == 'miercoles':
                mi_estudiantes_sin_recorrido=x.lugares_disponibles_x(vehiculo_id,turno,tipo)
                if mi_estudiantes_sin_recorrido == True:
                    actualizar = Miercoles(vehiculo=vehiculo, estudiante=estudiante, direccion=direccion,  viaje=viaje)

            if dia == 'jueves':
                mi_estudiantes_sin_recorrido=j.lugares_disponibles_j(vehiculo_id,turno,tipo)
                if mi_estudiantes_sin_recorrido == True:
                    actualizar = Jueves(vehiculo=vehiculo, estudiante=estudiante, direccion=direccion,  viaje=viaje)

            if dia == 'viernes':
                mi_estudiantes_sin_recorrido=v.lugares_disponibles_v(vehiculo_id,turno,tipo)
                if mi_estudiantes_sin_recorrido == True:
                    actualizar = Viernes(vehiculo=vehiculo, estudiante=estudiante, direccion=direccion,  viaje=viaje)

            actualizar.save()

            return redirect('recorridos', vehiculo_id=vehiculo.id, dia=dia)
        
        return render(request, self.template_name)

class CargarDirecciones(View):
    def get(self,request):
        id_alumno = request.GET.get('alumno')
                
        # Obtener el estudiante
        estudiante = Estudiante.objects.get(id=id_alumno)

        # Obtener las direcciones relacionadas con el estudiante
        direcciones = Direccion.objects.filter(id_familiar=estudiante.id_familiar)
        direcciones_lista = [
            {'id': direccion.id,
             'calle': direccion.calle,
             'altura': direccion.altura,              
             'piso': direccion.piso, 
             'dpto': direccion.dpto
             }
            for direccion in direcciones
        ]

        return JsonResponse({'direcciones': direcciones_lista})

class InfoVehiculoView(IndexView):
    template_name='ver_vehiculo.html'

    def get(self, request, *args, **kwargs):
        # En caso de que no se haya iniciado sesion redirige a login
        if not request.user.is_authenticated:
            return redirect('login')

        # Llamo al metodo get_context_data y paso los resultados
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehiculo_id = self.kwargs.get('vehiculo_id')

        vehiculo = Vehiculo.objects.get(id=vehiculo_id)
        print(vehiculo)

        context['vehiculo'] = vehiculo

        return context

class QuitarPasajero(View):
    template_name='mostrar_recorridos.html'
    def post(self, request, vehiculo_id, dia, viaje, estudiante):

        vehiculo = Vehiculo.objects.get(id=vehiculo_id)
        estudiante = Estudiante.objects.get(id=estudiante)
        viaje = Viaje.objects.get(id=viaje)

        if dia == 'lunes':
            resultado = Lunes.objects.filter(vehiculo__id=vehiculo.id, estudiante=estudiante, viaje=viaje).all()

        if dia == 'martes':
            resultado = Martes.objects.filter(vehiculo__id=vehiculo.id, estudiante=estudiante, viaje=viaje).all()

        if dia == 'miercoles':
            resultado = Miercoles.objects.filter(vehiculo__id=vehiculo.id, estudiante=estudiante, viaje=viaje).all()

        if dia == 'jueves':
            resultado = Jueves.objects.filter(vehiculo__id=vehiculo.id, estudiante=estudiante, viaje=viaje).all()

        if dia == 'viernes':
            resultado = Viernes.objects.filter(vehiculo__id=vehiculo.id, estudiante=estudiante, viaje=viaje).all()
        
        resultado.delete()
        
        return redirect('recorridos', vehiculo_id=vehiculo.id, dia=dia)