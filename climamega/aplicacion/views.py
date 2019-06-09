from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404

from .models import Catalogo

def index(request):
    return render(request, 'aplicacion/index.html')

# Create your views here.

def catalogo(request):
    listaProductos = Catalogo.objects.all()
    return render(request, 'aplicacion/catalogo.html', {'listaProductos': listaProductos})

def cotizacion(request, numero_cotizacion):
    respuesta = "Cotizacion Numero: %s."
    return HttpResponse(respuesta % numero_cotizacion)

def producto(request, codigo):
    try:
        producto = Catalogo.objects.get(pk=codigo)
    except Catalogo.DoesNotExist:
        raise Http404("No existe producto")
    return render(request, 'aplicacion/detalleProducto.html', {'producto': producto})
