from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404

from .models import Catalogo, Cotizacion, Prod_Cotizacion

def index(request):
    return render(request, 'aplicacion/index.html')

# Create your views here.

def catalogo(request):
    listaProductos = Catalogo.objects.all()
    return render(request, 'aplicacion/catalogo.html', {'listaProductos': listaProductos})

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

def producto(request, codigo):
    try:
        producto = Catalogo.objects.get(pk=codigo)
    except Catalogo.DoesNotExist:
        raise Http404("No existe producto")
    return render(request, 'aplicacion/detalleProducto.html', {'producto': producto})
