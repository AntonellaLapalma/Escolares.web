from apps.clientes.familias.models import *
from .models import *
from datetime import datetime
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.db.models import Sum

class Funciones_Ingresos:
    def actualizar(self):
        fecha_actual = datetime.now()
        mes_actual = fecha_actual.month
        anio_actual = fecha_actual.year

        familias = Familia.objects.filter(estado=True)
        registros = Ingreso.objects.filter(fecha__month=mes_actual, fecha__year=anio_actual)       
        
        for familia in familias:
            # en caso de que el id familiar no se encuentre en los 
            # registros de este mes se procede a realizar el registro
            try:
                # Intenta obtener un registro de Ingreso con el mismo id_familiar
                ingreso_existente = Ingreso.objects.get(id_familiar=familia.id_familiar,fecha__month=mes_actual, fecha__year=anio_actual)
            except Ingreso.DoesNotExist:
                # Si no existe, crea un nuevo registro
                f = Familia.objects.get(id_familiar=familia.id_familiar)
                registrar = Ingreso(id_familiar=f, fecha=fecha_actual, descuento=f.descuento, total=f.cuota)
                registrar.save()

            for registro in registros:
                # si el id se encuentra en el registro se actualizan los datos 
                # por si algun dato como descuento o la cuota fueron cambiados
                if familia.id_familiar == registro.id_familiar:
                    registro.total = familia.cuota
                    registro.descuento = familia.descuento
                    registro.fecha = fecha_actual
                    registro.save()

        # En caso de que uno haya sacado un cliente ya que dio de baja el servicio
        # y este no abonara la cuota del mes actual se podra tambien eliminar del ingreso 
        # en caso de que este ya haya sido agregado, es importante que el cambio 
        # se haga el mismo mes de la baja y no antes ni despues
        for registro in registros:
            if registro.id_familiar not in familias:
                eliminar=Ingreso.objects.get(id_familiar=familia.id_familiar)
                eliminar.delete()

    def anios(self):
        anios_unicos = Ingreso.objects.values('fecha__year').annotate(count=Count('fecha__year')).values_list('fecha__year', flat=True) # values trae los anios registrados y annotate cuenta cuantas veces se repite cada uno, values list obtiene valores unicos
        anios_unicos = list(set(anios_unicos)) # esta conversion asegura que se obtengan valores unicos

        return anios_unicos
    
    def convertir_mes(self, mes):
        meses = {1:'Enero',
                2:'Febrero',
                3:'Marzo',
                4:'Abril',
                5:'Mayo',
                6:'Junio',
                7:'Julio',
                8:'Agosto',
                9:'Septiembre',
                10:'Octubre',
                11:'Noviembre',
                12:'Diciembre'}
        
        return meses[mes]
    
    def calcular_facturacion_anual(self, anio):
        # inicialmente establezco la cantidad
        meses_del_anio = list(range(1, 13))
        # filtro segun el anio solicitado
        resultados = Ingreso.objects.filter(fecha__year=anio)
        # se agrupan los totales
        total_facturado_por_mes = (
            resultados
            .annotate(mes=ExtractMonth('fecha'))
            .values('mes')
            .annotate(total=Sum('total'))
            .order_by('mes')
        )
        # total facutrado
        total_por_mes = [
        {'mes': self.convertir_mes(mes), 'total': 0} for mes in meses_del_anio
        ]

        for item in total_facturado_por_mes:
            # Obtengo el nombre del mes
            nombre_mes = self.convertir_mes(item['mes'])
            # Buscar el objeto y actualizo el total
            for mes_dict in total_por_mes:
                if mes_dict['mes'] == nombre_mes:
                    mes_dict['total'] = item['total']
                    break

        return total_por_mes
    