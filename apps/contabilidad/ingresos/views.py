from django.shortcuts import render, redirect
from apps.home.views import IndexView
from .funciones_ingresos import *
from apps.contabilidad.precios.models import *
from django.db.models import Sum

class IngresosView(IndexView):
    template_name='mostrar_ingresos.html'

    def get(self,request,*args, **kwargs):
        # En caso de que no se haya iniciado sesion redirige a login
        if not request.user.is_authenticated:
            return redirect('login')
        
        # traigo los anios registrados para el navbar
        funciones = Funciones_Ingresos()      
        anios = funciones.anios()
        resultado = None
        total_recaudado = 0
        total_por_mes = 0
        total_recaudado_anualmente = 0

        # llamo el valor de la url
        anio = self.kwargs.get('anio_elegido')
        mes = self.kwargs.get('mes_elegido')

        if mes and anio:
            #filtro los datos para mostrar en pantalla
            resultado = Ingreso.objects.filter(fecha__year=anio, fecha__month=mes)
            mes = funciones.convertir_mes(mes)

            # calculo el ingreso total del mes 
            total_recaudado = resultado.aggregate(total_cuota=Sum('total'))
            # accedo al valor de la suma
            total_recaudado = total_recaudado['total_cuota']

            # ahora procedo a calcular el total de todos los meses de ese anio
            total_por_mes = funciones.calcular_facturacion_anual(anio)

            total_anual = Ingreso.objects.filter(fecha__year=anio)

            # calculo el ingreso total del anio 
            total_recaudado_anualmente = total_anual.aggregate(total_cuota2=Sum('total'))
            # accedo al valor de la suma
            total_recaudado_anualmente = total_recaudado_anualmente['total_cuota2']

        # precios vigentes para la tabla precios
        precios = Precio.objects.all()
        return render(request, self.template_name, {'anios':anios,
                                                    'resultado':resultado,
                                                    'total':total_recaudado,
                                                    'anio':anio,
                                                    'mes':mes,
                                                    'precios':precios,
                                                    'total_facturado':total_por_mes,
                                                    'total_anual':total_recaudado_anualmente})
    
    def post(self,request):
        if request.method == 'POST':
            funciones=Funciones_Ingresos()
            funciones.actualizar()
        return redirect('ingresos')