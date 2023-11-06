from typing import Any
from django.shortcuts import render, redirect
from apps.home.views import IndexView
from apps.contabilidad.sueldos.models import *
from .models import *
from apps.contabilidad.ingresos.funciones_ingresos import *
from .funciones_gastos import *

class GastosView(IndexView):
    template_name='mostrar_gastos.html'

    def get(self,request,*args, **kwargs):
        # En caso de que no se haya iniciado sesion redirige a login
        if not request.user.is_authenticated:
            return redirect('login')
        
        funciones2 = Funciones_Gastos()    
        resultado_empleados = None
        resultado_vehiculos = None
        total_por_mes = 0
        total_gastado_e = 0
        total_gastado_v = 0
        total_gastado_anualmente = 0

        anio = self.kwargs.get('anio_elegido')
        mes = self.kwargs.get('mes_elegido')

        if mes and anio:
            #filtro los datos para mostrar en pantalla
            resultado_empleados = Gastos_empleado.objects.filter(fecha__year=anio, fecha__month=mes)
            resultado_vehiculos = Gastos_vehiculo.objects.filter(fecha__year=anio, fecha__month=mes)

            # calculo el gasto total del mes 
            total_gastado_e = resultado_empleados.aggregate(total=Sum('total')) # aggregate realiza las agregaciones en un conjunto de resultados de una consulta
            total_gastado_v = resultado_vehiculos.aggregate(total=Sum('total'))

            # accedo al valor de la suma
            total_gastado_e = total_gastado_e['total']
            total_gastado_v = total_gastado_v['total']

            # ahora procedo a calcular el total de todos los meses de ese anio
            total_por_mes = funciones2.calcular_facturacion_anual(anio)

            # total anual
            resultado1 = Gastos_empleado.objects.filter(fecha__year=anio).aggregate(total=Sum('total'))
            resultado2 = Gastos_vehiculo.objects.filter(fecha__year=anio).aggregate(total=Sum('total'))

            total_anual_e = resultado1['total']
            total_anual_v = resultado2['total']

            if not total_anual_e:
                total_anual_e = 0

            if not total_anual_v:
                total_anual_v = 0

            # calculo el ingreso total del anio 
            total_gastado_anualmente = total_anual_e + total_anual_v
            funciones = Funciones_Ingresos()
            mes = funciones.convertir_mes(mes)#titulo de tarjeta
            if not total_gastado_v:
                total_gastado_v = 0
        # sueldos vigentes para la tabla precios
        sueldo = Puesto.objects.all()

        context = self.get_context_data()

        context['puestos']=sueldo
        context['anio']=anio
        context['mes']=mes
        context['resultado_empleados']=resultado_empleados
        context['resultado_vehiculos']=resultado_vehiculos
        context['total_empleados']=total_gastado_e
        context['total_vehiculos']=total_gastado_v
        context['total_gastado']=total_por_mes
        context['total_gastado_anualmente']=total_gastado_anualmente
        
        return render(request, self.template_name, context)
    
    def get_context_data(self,*args, **kwargs): # utilizandolo luego puedo heredar a registro el menu de anios sin repetir codigo
        funciones = Funciones_Ingresos() 
        anios = funciones.anios()
        context = super().get_context_data(**kwargs)
        context['anios']=anios

        return context
    
    def post(self,request,anio_elegido='',mes_elegido=''):
        if request.method == 'POST':
            funciones=Funciones_Gastos()
            funciones.actualizar()

            anio_elegido = self.kwargs.get('anio_elegido')
            mes_elegido = self.kwargs.get('mes_elegido')
            if  anio_elegido and mes_elegido:
                return redirect('gastos_anio_mes',mes_elegido,anio_elegido)
            
        return redirect('gastos')
    
class GEliminarView(GastosView):
    def post(self,request,anio_elegido,mes_elegido,id_registro,tabla):
        # llamo el valor de la url
        anio_elegido = self.kwargs.get('anio_elegido')
        mes_elegido = self.kwargs.get('mes_elegido')
        id_registro = self.kwargs.get('id_registro')
        tabla = self.kwargs.get('tabla')

        if  anio_elegido and mes_elegido and id_registro:
            if tabla == 'Vehiculo':
                elemento = Gastos_vehiculo.objects.get(id=id_registro)
            if tabla == 'Empleado':
                elemento = Gastos_empleado.objects.get(id=id_registro)
            elemento.delete()
            return redirect('gastos_anio_mes',mes_elegido,anio_elegido)
    
class RegistrarGastoView(GastosView):
    template_name='registrar_gasto.html'

    def get(self,request,*args, **kwargs):
        # En caso de que no se haya iniciado sesion redirige a login
        if not request.user.is_authenticated:
            return redirect('login')
        
        context = self.get_context_data(request, *args, **kwargs)

        return render(request, self.template_name, context)
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        vehiculos = Vehiculo.objects.all()
        motivos = Motivos_vehiculo.objects.all()
        context['vehiculos']=vehiculos
        context['motivos']=motivos

        return context

    def post(self,request,**kwargs):
        if request.method == 'POST':
            context = self.get_context_data(**kwargs)
            error = None
            error_x = None
            vehiculo = request.POST.get('opcion_vehiculo')
            motivo = request.POST.get('motivo_vehiculo')
            total = request.POST.get('total_vehiculo')

            agregar = Funciones_Gastos()
            validar = agregar.validar_total(total)
            print(total.isdigit())

            if  vehiculo and motivo:
                if vehiculo.isdigit() and motivo.isdigit():
                    vehiculo = Vehiculo.objects.get(id=vehiculo)
                    motivo = Motivos_vehiculo.objects.get(id=motivo)
                    if validar:
                        agregar.registrar(vehiculo,motivo,total)
                        return redirect('gastos')
                    else:
                        error='Ingrese solo números enteros.*'
                else:
                    error_x='Error, vuelva a intentarlo.*'            
            if not validar:
                error='Ingrese solo números enteros.*'

            context['error_total']=error
            context['error_x']=error_x


        return render(request, self.template_name, context)

class ModificarSueldosView(GastosView):
    template_name = 'modificar_sueldos.html'
    def get(self,request,*args, **kwargs):
        # En caso de que no se haya iniciado sesion redirige a login
        if not request.user.is_authenticated:
            return redirect('login')
        
        context = self.get_context_data(request, *args, **kwargs)
        puesto1 = self.kwargs.get('puesto_elegido')
        puesto = Puesto.objects.get(puesto=puesto1)

        context['puesto']=puesto

        return render(request, self.template_name, context)
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
    
    def post(self,request, *args, **kwargs):
        context = self.get_context_data(request, *args, **kwargs)

        puesto1 = self.kwargs.get('puesto_elegido')
        puesto = Puesto.objects.get(puesto=puesto1)
        total = request.POST.get('total_sueldo')
        print(total)
        f=Funciones_Gastos()
        val=f.validar_total(total)
        if val:
            puesto.sueldo = total
            puesto.save()
            return redirect('gastos')
        else:
            error='Ingrese solo números enteros.*'

        context['error']=error
        context['puesto']=puesto
        return render(request, self.template_name, context)
