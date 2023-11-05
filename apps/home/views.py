from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from datetime import datetime
from apps.contabilidad.ingresos.funciones_ingresos import *
from apps.contabilidad.gastos.funciones_gastos import *
from apps.clientes.adultos.models import *
from apps.clientes.estudiantes.models import *
from apps.recorridos.models import *
from .funciones_inicio import *

import json

class IndexView(TemplateView):
    template_name='index.html'

class InicioView(IndexView):
    template_name='inicio.html'
    
    def get(self,request,*args, **kwargs):
        # En caso de que no se haya iniciado sesion redirige a login
        if not request.user.is_authenticated:
            return redirect('login')
        
        fecha_actual = datetime.now()
        anio_actual = fecha_actual.year

        #ingresos
        funciones = Funciones_Ingresos()
        datos_anuales = funciones.calcular_facturacion_anual(anio_actual)
        datos_ingreso = [i['total'] for i in datos_anuales]
        datos_ingreso = json.dumps(datos_ingreso)

        #gastos
        funciones2 = Funciones_Gastos()
        datos_anuales2 = funciones2.calcular_facturacion_anual(anio_actual)
        datos_gastos = [i['total'] for i in datos_anuales2]
        datos_gastos = json.dumps(datos_gastos)

        #familias total
        familia = Familia.objects.count()
        #padres total
        padres = Adulto.objects.count()
        #estudiantes total
        estudiante = Estudiante.objects.count()
        #empleados total
        empleado = Empleado.objects.count()
        #choferes total
        chofer = Empleado.objects.filter(puesto__puesto='Chofer').count()
        #celadores total
        celador = Empleado.objects.filter(puesto__puesto='Celador').count()
        #vehiculos total
        vehiculo = Vehiculo.objects.count()

        #recorridos total
        fr=Funciones_Inicio()
        l = fr.calcular_recorrdido(Lunes)
        m = fr.calcular_recorrdido(Martes)
        x = fr.calcular_recorrdido(Miercoles)
        j = fr.calcular_recorrdido(Jueves)
        v = fr.calcular_recorrdido(Viernes)
        recorrido = l+m+x+j+v


        return render (request, self.template_name, {'anio':anio_actual,
                                                     'familia':familia,
                                                     'adulto':padres,
                                                     'estudiante':estudiante,
                                                     'empleado':empleado,
                                                     'chofer':chofer,
                                                     'celador':celador,
                                                     'vehiculo':vehiculo,
                                                     'recorrido':recorrido,
                                                     'datos_ingreso':datos_ingreso,
                                                     'datos_gastos':datos_gastos})
        