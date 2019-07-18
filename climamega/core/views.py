from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.utils import timezone
from django.http import HttpRequest


from functools import reduce

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
import time


from .models import Catalogo, Cotizacion, Prod_Cotizacion, Cliente, Estado, Venta


def index(request):
    return render(request, 'core/index.html')

def detalleCliente(request, rut):
    try:
        cliente = Cliente.objects.get(pk=rut)
    except Cliente.DoesNotExist:
        return render(request, 'core/detalleCliente.html', {'cliente': False})
    return render(request, 'core/detalleCliente.html', {'cliente': cliente})


def buscarCliente(request):
    if request.method == 'POST' and request.POST['rut'] != "":
        try:
            cliente = Cliente.objects.get(pk=request.POST['rut'])
        except Cliente.DoesNotExist:
            return render(request, 'core/detalleCliente.html', {'cliente': False})
        return render(request, 'core/detalleCliente.html', {'cliente': cliente})
    else:
        listaClientes = Cliente.objects.all()
        return render(request, 'core/clientesbus.html', {'listaClientes': listaClientes})


def generarCliente(request):
    Cliente.objects.create(rut=request.POST['rut'],
                           nombre=request.POST['nombre'],
                           apellido=request.POST['apellido'],
                           correo=request.POST['email'],
                           telefono=request.POST['telefono'],
                           direccion=request.POST['direccion']
                           )
    return render(request, 'core/index.html')


def eliminarCliente(request):
    if request.method == 'POST' and request.POST.get('rut', False):
        try:
            cliente = Cliente.objects.get(pk=request.POST['rut'])
        except Cliente.DoesNotExist:
            return render(request, 'core/confirmarEliminarCliente.html', {'cliente': False})
        return render(request, 'core/confirmarEliminarCliente.html', {'cliente': cliente})
    else:
        return render(request, 'core/clienteseli.html')


def confirmarEliminarCliente(request, rut):
    Cliente.objects.filter(pk=rut).delete()
    return render(request, 'core/index.html')


def modificarCliente(request):
    if request.method == 'POST' and request.POST.get('rut', False):
        try:
            cliente = Cliente.objects.get(pk=request.POST['rut'])
        except Cliente.DoesNotExist:
            return render(request, 'core/confirmarModificarCliente.html', {'cliente': False})
        return render(request, 'core/confirmarModificarCliente.html', {'cliente': cliente})
    else:
        return render(request, 'core/clientesmodi.html')


def confirmarModificarCliente(request, rut):
    if request.POST.get('nombre', False) and request.POST.get('apellido', False) and request.POST.get('direccion', False):
        Cliente.objects.filter(pk=rut).update(
          nombre=request.POST['nombre'],
          apellido=request.POST['apellido'],
          correo=request.POST['email'],
          telefono=request.POST['telefono'],
          direccion=request.POST['direccion']
        )
        return render(request, 'core/index.html')
    else:
        return render(request, 'core/clientesmodi.html')
    
    


def nuevaCotizacion(request):
    if request.method == 'POST' and request.POST.get('expiracion', False) and request.POST.get('cliente', False):
      try:
          cantidad = list(map(lambda cantidad: int(cantidad), request.POST.getlist('productos')))
          productos = list(Catalogo.objects.all())

          productosCantidad = list(filter(lambda pc: int(pc[1]) > 0, zip(productos, cantidad)))

          productos, cantidades = zip(*productosCantidad)

          precioTotal = 0
          for i in productosCantidad:
            precioTotal += i[0].precio * i[1]

          precioServicio = int(request.POST['servicio'])

          request.session['rut'] = request.POST['cliente']
          request.session['expiracion'] = request.POST['expiracion']
          request.session['servicio'] = request.POST['servicio']
          request.session['productos'] = list(map(lambda p: p.codigo, productos))
          request.session['cantidades'] = cantidades
          request.session['total'] = precioTotal + precioServicio

          context = { 'rut': request.POST['cliente'],
                      'expiracion': request.POST['expiracion'],
                      'servicio': request.POST['servicio'],
                      'productosCantidad': productosCantidad,
                      'total': precioTotal + precioServicio}

          return render(request, 'core/confirmarCotizacion.html', context)
        
      except KeyError:
          listaProductos = Catalogo.objects.all()
          listaClientes = Cliente.objects.all()

          context = {
              'listaProductos': listaProductos,
              'listaClientes': listaClientes
          }
          return render(request, 'core/cotizacionagre.html', context)
    else:

        listaProductos = Catalogo.objects.all()
        listaClientes = Cliente.objects.all()

        context = {
            'listaProductos': listaProductos,
            'listaClientes': listaClientes
        }
        return render(request, 'core/cotizacionagre.html', context)


def crearCotizacion(request):
    cotizacion = Cotizacion.objects.create(
            rut_cliente=Cliente.objects.get(pk=request.session['rut']),
            emision=timezone.now(),
            expiracion=request.session['expiracion'],
            precio_servicio=request.session['servicio'],
            total=request.POST['total'],
            estado=Estado.objects.get(pk=1)
        )
    
    for codProducto, cantidad in zip(request.session['productos'], request.session['cantidades']):
        Prod_Cotizacion.objects.create(
            cotizacion=cotizacion,
            codigoProducto=Catalogo.objects.get(pk=codProducto),
            cantidad=cantidad)

    return buscarCotizacion(HttpRequest())



def buscarCotizacion(request):
    if request.method == 'POST':
        rut = request.POST['numero-rut']
        cotizacion = request.POST['numero-cotizacion']
        listaCotizaciones = []
        if rut:
            listaCotizaciones = Cotizacion.objects.filter(
              rut_cliente = rut
            )
        if cotizacion:
            listaCotizaciones = Cotizacion.objects.filter(
              numero_cotizacion = cotizacion
            )
        return render(request, 'core/cotizacionbus.html', {'listaCotizaciones': listaCotizaciones})
    else:
        listaCotizaciones = Cotizacion.objects.all()
        return render(request, 'core/cotizacionbus.html', {'listaCotizaciones': listaCotizaciones})


def detalleCotizacion(request, codigo):
    cotizacion = Cotizacion.objects.get(pk=codigo)
    cotizacion.productos.all()
    cotizacion.rut_cliente.apellido
    cotizacion.rut_cliente.nombre
    for registro in cotizacion.prod_cotizacion_set.all():
      print (registro.cantidad)
    return render(request, 'core/detalleCotizacion.html', {'cotizacion': cotizacion})



def agregarProducto(request):
  if  request.method == 'POST' and request.POST.get('nombre', False) and request.POST.get('descripcion', False) and request.POST.get('precio', False):
      Catalogo.objects.create(nombre=request.POST['nombre'],
                            precio=request.POST['precio'],
                            descripcion=request.POST['descripcion'])
      return render(request, 'core/index.html')

  else:
      return render(request, 'core/catalogoagre.html')
    

def buscarCatalogo(request):
    listaProductos = Catalogo.objects.all()
    return render(request, 'core/catalogobus.html', {'listaProductos': listaProductos})


def detalleProducto(request, codigo):
    producto = Catalogo.objects.get(pk=codigo)
    return render(request, 'core/detalleProducto.html', {'producto': producto})


def modificarProducto(request):
    listaProductos = Catalogo.objects.all()
    return render(request, 'core/catalogomodi.html', {'listaProductos': listaProductos})


def confirmarModificarProducto(request, codigo):
    if  request.method == 'POST':
        Catalogo.objects.filter(pk=codigo).update(
          nombre=request.POST['nombre'],
          descripcion=request.POST['descripcion'],
          precio=request.POST['precio']
        )
        return render(request, 'core/index.html')
    else:
        producto = Catalogo.objects.get(pk=codigo)
        return render(request, 'core/confirmarModificarProducto.html', {'producto': producto})


def eliminarProducto(request):
    listaProductos = Catalogo.objects.all()
    return render(request, 'core/catalogoeli.html', {'listaProductos': listaProductos})


def confirmarEliminarProducto(request, codigo):
    if  request.method == 'POST':
        Catalogo.objects.filter(pk=codigo).delete()
        return render(request, 'core/index.html')
    else:
        producto = Catalogo.objects.get(pk=codigo)
        return render(request, 'core/confirmarEliminarProducto.html', {'producto': producto})


def aceptarCotizacion(request, codigo):
    Venta.objects.create( cotizacion = Cotizacion.objects.get(pk=codigo),
                          fechaEmision = timezone.now())

    return ventas(request)


def ventas(request):
    ventas = Ventas.objects.all()
    return render(request, 'core/ventas.html', {'ventas': ventas})