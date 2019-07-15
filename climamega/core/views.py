from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.utils import timezone

from .models import Catalogo, Cotizacion, Prod_Cotizacion, Cliente, Servicio, Estado


def index(request):
    return render(request, 'core/index.html')

def catalogo(request):
    listaProductos = Catalogo.objects.all()
    return render(request, 'core/catalogo.html', {'listaProductos': listaProductos})

def producto(request, codigo):
    try:
        producto = Catalogo.objects.get(pk=codigo)
    except Catalogo.DoesNotExist:
        raise Http404("No existe producto")
    return render(request, 'core/detalleProducto.html', {'producto': producto})

def clientes(request):
    listaClientes = Cliente.objects.all()
    return render(request, 'core/clientes.html', {'listaClientes': listaClientes})

def cliente(request, rut):
    try:
        cliente = Cliente.objects.get(pk=rut)
    except Cliente.DoesNotExist:
        raise Http404("No existe cliente")
    return render(request, 'core/detalleCliente.html', {'cliente': cliente})

def nuevoCliente(request):
    return render(request, 'core/nuevoCliente.html')

def generarCliente(request):
    Cliente.objects.create( rut = request.POST['rut'],
                            nombre = request.POST['nombre'],
                            apellido = request.POST['apellido'],
                            correo = request.POST['correo'],
                            telefono = request.POST['telefono'],
                            direccion = request.POST['direccion']
                            )

    listaClientes = Cliente.objects.all()
    return render(request, 'core/clientes.html', {'listaClientes': listaClientes})




def cotizaciones(request):
    listaCotizaciones = Cotizacion.objects.all()
    return render(request, 'core/cotizaciones.html', {'listaCotizaciones': listaCotizaciones})


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
    return render(request, 'core/detalleCotizacion.html', context)


def nuevaCotizacion(request):
    listaProductos = Catalogo.objects.all()
    listaClientes = Cliente.objects.all()
    
    context = {
      'listaProductos': listaProductos,
      'listaClientes': listaClientes
    }
    return render(request, 'core/nuevaCotizacion.html', context)


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

    context = {
      'cotizacion': cotizacion,
      'listaProductos': cotizacion.prod_cotizacion_set.all()
    }
    return render(request, 'core/detalleCotizacion.html', context)

def nuevoProducto(request):
    return render(request, 'core/nuevoProducto.html')


def generarProducto(request):
    Catalogo.objects.create( nombre = request.POST['nombre'],
                             precio = request.POST['precio'])

    listaProductos = Catalogo.objects.all()
    return render(request, 'core/catalogo.html', {'listaProductos': listaProductos})


