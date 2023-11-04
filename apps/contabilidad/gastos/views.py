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
        
        funciones = Funciones_Ingresos() 
        funciones2 = Funciones_Gastos()    
        anios = funciones.anios()
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
            total_gastado_e = resultado_empleados.aggregate(total=Sum('total'))
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

            # calculo el ingreso total del anio 
            if total_anual_e and total_anual_v:
                total_gastado_anualmente = total_anual_e + total_anual_v
                total_gastado_anualmente = total_gastado_anualmente['total']
            # accedo al valor de la suma
            
            mes = funciones.convertir_mes(mes)#titulo de tarjeta
            if not total_gastado_v:
                total_gastado_v = 0
        # sueldos vigentes para la tabla precios
        sueldo = Puesto.objects.all()
        
        return render(request, self.template_name, {'anios':anios,
                                                    'puestos':sueldo,
                                                    'anio':anio,
                                                    'mes':mes,
                                                    'resultado_empleados':resultado_empleados,
                                                    'resultado_vehiculos':resultado_vehiculos,
                                                    'total_empleados':total_gastado_e,
                                                    'total_vehiculos':total_gastado_v,
                                                    'total_gastado':total_por_mes,
                                                    'total_gastado_anualmente':total_gastado_anualmente,})
    
    def post(self,request):
        if request.method == 'POST':
            funciones=Funciones_Gastos()
            funciones.actualizar()
        return redirect('gastos')