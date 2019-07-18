from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.utils import timezone

from .models import Catalogo, Cotizacion, Prod_Cotizacion, Cliente, Estado


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
    if request.method == 'POST' and request.POST['rut'] != "":
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
    if request.method == 'POST' and request.POST['rut'] != "":
        try:
            cliente = Cliente.objects.get(pk=request.POST['rut'])
        except Cliente.DoesNotExist:
            return render(request, 'core/confirmarModificarCliente.html', {'cliente': False})
        return render(request, 'core/confirmarModificarCliente.html', {'cliente': cliente})
    else:
        return render(request, 'core/clientesmodi.html')


def confirmarModificarCliente(request, rut):
    Cliente.objects.filter(pk=rut).update(
      nombre=request.POST['nombre'],
      apellido=request.POST['apellido'],
      correo=request.POST['email'],
      telefono=request.POST['telefono'],
      direccion=request.POST['direccion']
    )
    return render(request, 'core/index.html')


def nuevaCotizacion(request):
    if request.method == 'POST' and request.POST['cliente'] != "" and request.POST.getlist('productos') != [] and request.POST['fecha-expiracion'] != "":
        cotizacion = Cotizacion.objects.create(
            rut_cliente=Cliente.objects.get(pk=request.POST['cliente']),
            emision=timezone.now(),
            expiracion=request.POST['fecha-expiracion'],
            precio_servicio=request.POST['precio-servicio'],
            total=request.POST['total'],
            estado=Estado.objects.get(pk=1))

        cantidad = list(map(lambda cantidad: int(cantidad), request.POST.getlist('productos')))
        productos = list(Catalogo.objects.all())

        listaProductosCantidad = list(filter(lambda tp: int(tp[1]) > 0, zip(productos, cantidad)))
        for (producto, cantidad) in listaProductosCantidad:
            Prod_Cotizacion.objects.create(
                cotizacion=cotizacion,
                codigoProducto=producto,
                cantidad=cantidad)

        return render(request, 'core/index.html')
        
    else:
        listaProductos = Catalogo.objects.all()
        listaClientes = Cliente.objects.all()

        context = {
            'listaProductos': listaProductos,
            'listaClientes': listaClientes
        }
        return render(request, 'core/cotizacionagre.html', context)


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











def nuevoProducto(request):
    return render(request, 'core/nuevoProducto.html')


def generarProducto(request):
    Catalogo.objects.create(nombre=request.POST['nombre'],
                            precio=request.POST['precio'])

    listaProductos = Catalogo.objects.all()
    return render(request, 'core/catalogo.html', {'listaProductos': listaProductos})


def catalogo(request):
    return render(request, 'core/catalogobus.html')


def busquedaCatalogo(request):
    codigo = request.POST['numero-producto']
    return render(request, 'core/detalleProducto.html', {'producto': codigo})


def producto(request, codigo):
    try:
        producto = Catalogo.objects.get(pk=codigo)
    except Catalogo.DoesNotExist:
        raise Http404("No existe producto")
    return render(request, 'core/detalleProducto.html', {'producto': producto})
