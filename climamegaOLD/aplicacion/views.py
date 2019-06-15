from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.utils import timezone


from .models import Catalogo, Cotizacion, Prod_Cotizacion, Cliente, Servicio, Estado

def index(request):
    return render(request, 'aplicacion/index.html')

# Create your views here.

def catalogo(request):
    listaProductos = Catalogo.objects.all()
    return render(request, 'aplicacion/catalogo.html', {'listaProductos': listaProductos})

def producto(request, codigo):
    try:
        producto = Catalogo.objects.get(pk=codigo)
    except Catalogo.DoesNotExist:
        raise Http404("No existe producto")
    return render(request, 'aplicacion/detalleProducto.html', {'producto': producto})


def cotizaciones(request):
    listaCotizaciones = Cotizacion.objects.all()
    return render(request, 'aplicacion/cotizaciones.html', {'listaCotizaciones': listaCotizaciones})


def cotizacion(request, numero_cotizacion):
    try:
        cotizacion = Cotizacion.objects.get(pk=numero_cotizacion)
        listaProductos = cotizacion.prod_cotizacion_set.all()
    except Cotizacion.DoesNotExist:
        raise Http404("No existe cotizacion")
    context = {
      'cotizacion': cotizacion,
      'listaProductos': listaProductos
    }
    return render(request, 'aplicacion/detalleCotizacion.html', context)


def nuevaCotizacion(request):
    listaProductos = Catalogo.objects.all()
    listaClientes = Cliente.objects.all()
    context = {
      'listaProductos': listaProductos,
      'listaClientes': listaClientes
    }
    return render(request, 'aplicacion/nuevaCotizacion.html', context)


def generarCotizacion(request):
    cotizacion = Cotizacion.objects.create( rut_cliente=Cliente.objects.get(pk=request.POST['cliente']),
                                            tipo_servicio = Servicio.objects.get(pk=1),
                                            emision = timezone.now(),
                                            expiracion = timezone.now(),
                                            total = 120000,
                                            precio_servicio = 30000,
                                            estado = Estado.objects.get(pk=1))

    listaProductos = request.POST.getlist('productos')

    for producto in listaProductos:
        Prod_Cotizacion.objects.create( cotizacion = cotizacion, 
                                        codigoProducto = Catalogo.objects.get(pk=producto), 
                                        cantidad = 1)

    numeroCotizacion = cotizacion.numero_cotizacion

    context = {
      'cotizacion': cotizacion,
      'listaProductos': cotizacion.prod_cotizacion_set.all()
    }
    return render(request, 'aplicacion/detalleCotizacion.html', context)


