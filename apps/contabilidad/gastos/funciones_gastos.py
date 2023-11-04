from apps.empleados.models import *
from apps.contabilidad.ingresos.funciones_ingresos import *
from .models import *
from datetime import datetime
from django.db.models.functions import ExtractMonth
from django.db.models import Sum
from django.db.models import F

class Funciones_Gastos:
    def actualizar(self):
        fecha_actual = datetime.now()
        mes_actual = fecha_actual.month
        anio_actual = fecha_actual.year

        empleados = Empleado.objects.filter(puesto__isnull=False)
        registros_empleados = Gastos_empleado.objects.filter(fecha__month=mes_actual, fecha__year=anio_actual)   

        for empleado in empleados:
            try:
                ingreso_existente = Gastos_empleado.objects.get(id_empleado=empleado.id)  
            except Gastos_empleado.DoesNotExist:
                e = Empleado.objects.get(id=empleado.id)
                registrar = Gastos_empleado(id_empleado=e, fecha=fecha_actual, total=e.puesto.sueldo) 
                registrar.save()

            for registro in registros_empleados:
                if empleado.id == registro.id:
                    registro.total = empleado.puesto.sueldo
                    registro.fecha = fecha_actual
                    registro.save()

    def calcular_facturacion_anual(self, anio):
        # inicialmente establezco la cantidad
        meses_del_anio = list(range(1, 13))
        # filtro segun el anio solicitado
        resultados1 = Gastos_empleado.objects.filter(fecha__year=anio)
        resultados2 = Gastos_vehiculo.objects.filter(fecha__year=anio)
        # se agrupan los totales
        total_facturado_por_mes1 = (
            resultados1
            .annotate(mes=ExtractMonth('fecha'))
            .values('mes')
            .annotate(total=Sum('total'))
            .order_by('mes')
        )
        total_facturado_por_mes2 = (
            resultados2
            .annotate(mes=ExtractMonth('fecha'))
            .values('mes')
            .annotate(total=Sum('total'))
            .order_by('mes')
        )
        c=Funciones_Ingresos()
        # total facutrado
        total_por_mes = [
        {'mes': c.convertir_mes(mes), 'total': 0} for mes in meses_del_anio
        ]

        for item in total_facturado_por_mes1:
            # Obtengo el nombre del mes
            nombre_mes = c.convertir_mes(item['mes'])
            # Buscar el objeto y actualizo el total
            for mes_dict in total_por_mes:
                if mes_dict['mes'] == nombre_mes:
                    mes_dict['total'] = item['total']
                    break
        
        for item in total_facturado_por_mes2:
            # Obtengo el nombre del mes
            nombre_mes = c.convertir_mes(item['mes'])
            # Buscar el objeto y actualizo el total
            for mes_dict in total_por_mes:
                if mes_dict['mes'] == nombre_mes:
                    mes_dict['total'] = mes_dict['total'] + item['total']
                    break

        return total_por_mes

