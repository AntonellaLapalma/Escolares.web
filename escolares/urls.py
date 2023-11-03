"""escolares URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.login.views import *
from apps.home.views import *
from apps.clientes.familias.views import *
from apps.empleados.views import *
from apps.vehiculos.views import *
from apps.recorridos.views import *
from apps.contabilidad.ingresos.views import *
from apps.contabilidad.gastos.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', InicioView.as_view(), name='inicio'),
    path('login/', LoginView.as_view(), name='login'),

    path('clientes/',ClientesView.as_view(),name='clientes'),
    path('clientes/', ClientesView.as_view(), name='clientes'),
    path('clientes/<str:busqueda>/', ClientesView.as_view(), name='buscar_clientes'),
    path('clientes/filtro/<str:estado>', ClientesView.as_view(), name='clientes_estado'),
    path('clientes/registrar', RegistrarClienteView.as_view(), name='registrar_cliente'),
    path('clientes/modificar/<int:familia_id>/', ModificarGrupoFamiliar.as_view(), name='modificar_cliente'),
    path('clientes/eliminar/<int:familia_id>/', EliminarGrupoFamiliarView.as_view(), name='eliminar_cliente'),
    path('cargar-divisiones/', CargarDivisionesView.as_view(), name='cargar_divisiones'),

    path('empleados/', EmpleadosView.as_view(), name='empleados'),
    path('empleados/<str:busqueda>/', EmpleadosView.as_view(), name='buscar_empleados'),
    path('empleados/filtro/<str:estado>', EmpleadosView.as_view(), name='empleados_estado'),
    path('empleados/registrar', RegistrarEmpleadoView.as_view(), name='registrar_empleado'),
    path('empleados/modificar/<int:empleado_id>/', ModificarEmpleadoView.as_view(), name='modificar_empleado'),
    path('empleados/eliminar/<int:empleado_id>/', EliminarEmpleadoView.as_view(), name='eliminar_empleado'),

    path('vehiculos/', VehiculosView.as_view(), name='vehiculos'),
    path('vehiculos/<str:busqueda>/', VehiculosView.as_view(), name='buscar_vehiculos'),
    path('vehiculos/filtro/<str:estado>', VehiculosView.as_view(), name='vehiculos_estado'),
    path('vehiculos/registrar', RegistrarVehiculoView.as_view(), name='registrar_vehiculo'),
    path('vehiculos/modificar/<int:vehiculo_id>/', ModificarVehiculoView.as_view(), name='modificar_vehiculo'),
    path('vehiculos/eliminar/<int:vehiculo_id>/', EliminarVehiculoView.as_view(), name='eliminar_vehiculo'),

    path('vehiculos/<int:vehiculo_id>/recorrido/<str:dia>/', RecorridosView.as_view(), name='recorridos'),
    path('cargar-direcciones/', CargarDirecciones.as_view(), name='cargar_direcciones'),
    path('vehiculos/<int:vehiculo_id>/info/', InfoVehiculoView.as_view(), name='ver_info_vehiculo'),
    path('vehiculos/quitar-pasajero/<int:vehiculo_id>/<str:dia>/<str:viaje>/<str:estudiante>/', QuitarPasajero.as_view(), name='quitar-pasajero'),
    
    path('ingresos/', IngresosView.as_view(), name='ingresos'),
    path('ingresos/<int:anio_elegido>/<int:mes_elegido>/', IngresosView.as_view(), name='ingresos_anio_mes'),

    path('gastos/', GastosView.as_view(), name='gastos'),
]
