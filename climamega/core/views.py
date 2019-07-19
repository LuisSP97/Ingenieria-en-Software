import os
import time
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.utils import timezone
from django.http import HttpRequest
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors

this_path = os.getcwd() + '/core/'
from .models import Catalogo, Cotizacion, Prod_Cotizacion, Cliente, Estado, Venta
from functools import reduce
import io
from django.http import FileResponse

def index(request):
    return render(request, 'core/index.html')

def detalleCliente(request, rut):
    try:
        cliente = Cliente.objects.get(pk=rut)
    except Cliente.DoesNotExist:
        return render(request, 'core/detalleCliente.html', {'cliente': False})
    return render(request, 'core/detalleCliente.html', {'cliente': cliente})


def buscarCliente(request):
    if request.method == 'POST' and request.POST.get('rut', False):
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
    return render(request, 'core/generarReporte.html', { 'cotizacion' : cotizacion.numero_cotizacion })



def buscarCotizacion(request):
    listaCotizaciones = Cotizacion.objects.all()
    if request.method == 'POST':
        if request.POST.get('rut', False):
            listaCotizaciones = Cotizacion.objects.filter(
              rut_cliente = request.POST['rut'])
        if request.POST.get('cotizacion', False):
            listaCotizaciones = Cotizacion.objects.filter(
              numero_cotizacion = request.POST['cotizacion']
            )
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
    productos = Catalogo.objects.all()
    if  request.method == 'POST':
        if request.POST.get('nombre', False):
            productos = productos.filter(nombre__contains = request.POST['nombre'])
        if request.POST.get('descripcion', False):
            productos = productos.filter(descripcion__contains = request.POST['descripcion'])
        if request.POST.get('precioI', False):
            productos = productos.filter(fechaEmision__gte = request.POST['precioI'])
        if request.POST.get('precioF', False):
            productos = productos.filter(fechaEmision__lte = request.POST['precioF'])

    return render(request, 'core/catalogobus.html', { 'listaProductos': productos.order_by('nombre') })


def detalleProducto(request, codigo):
    producto = Catalogo.objects.get(pk=codigo)
    return render(request, 'core/detalleProducto.html', {'producto': producto})


def modificarProducto(request):
    productos = Catalogo.objects.all()
    if  request.method == 'POST':
        if request.POST.get('nombre', False):
            productos = productos.filter(nombre__contains = request.POST['nombre'])
        if request.POST.get('descripcion', False):
            productos = productos.filter(descripcion__contains = request.POST['descripcion'])
        if request.POST.get('precioI', False):
            productos = productos.filter(fechaEmision__gte = request.POST['precioI'])
        if request.POST.get('precioF', False):
            productos = productos.filter(fechaEmision__lte = request.POST['precioF'])

    return render(request, 'core/catalogomodi.html', { 'listaProductos': productos.order_by('nombre') })



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
    productos = Catalogo.objects.all()
    if  request.method == 'POST':
        if request.POST.get('nombre', False):
            productos = productos.filter(nombre__contains = request.POST['nombre'])
        if request.POST.get('descripcion', False):
            productos = productos.filter(descripcion__contains = request.POST['descripcion'])
        if request.POST.get('precioI', False):
            productos = productos.filter(fechaEmision__gte = request.POST['precioI'])
        if request.POST.get('precioF', False):
            productos = productos.filter(fechaEmision__lte = request.POST['precioF'])

    return render(request, 'core/catalogoeli.html', { 'listaProductos': productos.order_by('nombre') })


def confirmarEliminarProducto(request, codigo):
    if  request.method == 'POST':
        Catalogo.objects.filter(pk=codigo).delete()
        return render(request, 'core/index.html')
    else:
        producto = Catalogo.objects.get(pk=codigo)
        return render(request, 'core/confirmarEliminarProducto.html', {'producto': producto})


def aceptarCotizacion(request, codigo):
    if Venta.objects.filter(cotizacion = Cotizacion.objects.get(pk=codigo)):
        return ventas(request)

    Venta.objects.create( cotizacion = Cotizacion.objects.get(pk=codigo),
                          fechaEmision = timezone.now())

    Cotizacion.objects.filter(pk=codigo).update(
          estado = Estado.objects.get(pk=2)
        )
    return ventas(request)


def eliminarCotizacion(request, codigo):
    if Venta.objects.filter(cotizacion = Cotizacion.objects.get(pk=codigo)):
        print ("asdasdasdasddasd")
        return buscarCotizacion(HttpRequest())
    Cotizacion.objects.filter(pk=codigo).delete()

    return buscarCotizacion(HttpRequest())


def ventas(request):
    ventas = Venta.objects.all()
    if  request.method == 'POST':
        if request.POST.get('rut', False):
            ventas = ventas.filter(cotizacion__rut_cliente__rut = request.POST['rut'])
        if request.POST.get('fechaI', False):
            ventas = Venta.objects.filter(fechaEmision__gte = request.POST['fechaI'])
        if request.POST.get('fechaF', False):
            ventas = Venta.objects.filter(fechaEmision__lte = request.POST['fechaF'])

    return render(request, 'core/ventas.html', { 'ventas': ventas.order_by('-fechaEmision') })


def detalleVenta(request, codigo):
    venta = Venta.objects.get(pk=codigo)
    return render(request, 'core/detalleVenta.html', {'venta': venta})


#SE INSTALO CANVAS, REPORTLAB MEDIANTE PIP

def reporte(request, codigo):
    cotizacion = Cotizacion.objects.get(pk=codigo)
    #CREA LA RESPUESTA PARA EL PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Cotizacion-' + str(cotizacion.numero_cotizacion) + '.pdf'
    #CREA EL PDF
    buffer = BytesIO() #ES UN BUFFER, DONDE SE GUARDARAN LOS DATOS
    c = canvas.Canvas(buffer, pagesize=A4)

    #HEADER
    c.setLineWidth(.3)
    c.setFont('Helvetica', 22)
    c.drawString(30,750,'ClimaMega')

    c.setFont('Helvetica', 12)
    c.drawString(30,735,'Cotizacion')

    c.setFont('Helvetica',12)
    c.drawString(480,750,'Fecha')
    c.drawString(480,735,str(timezone.now().date()))
    c.line(460,747,560,747)

    #datos empresa

    rut = "R.U.T 76.945.022-k" 
    nomComercial = "Clima-Mega SpA"

    tel = "Teléfono +569 9246 70 43  -  +569 7410 7920"
    correo = "Correo ventas@megaclima.cl  -  elizabeth@megaclima.cl"

    c.drawString(30,715, rut)
    c.drawString(30,695, nomComercial)
    c.drawString(30,675, tel)
    c.drawString(30,655, correo)



    #estilo
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontsize = 10

    b1 = Paragraph('''Producto''', styleBH)
    b2 = Paragraph('''Precio Unitario''', styleBH)
    b3 = Paragraph('''Cantidad''', styleBH)
    b4 = Paragraph('''Total''', styleBH)
    
    data = [([b1], [b2], [b3], [b4])]

    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7

    high = 600

    for producto in cotizacion.prod_cotizacion_set.all():
      nombre = producto.codigoProducto.nombre
      precio = producto.codigoProducto.precio
      cantidad = producto.cantidad
      total = precio * cantidad
      data.append([str(nombre), str(precio), str(cantidad), str(total)])
      high = high - 18

    data.append(["Servicio", "", "", str(cotizacion.precio_servicio)])
    data.append(["Precio total", "", "", str(cotizacion.total)])
    high -= 36
    width, height = A4
    
    table = Table(data, colWidths = [10 * cm, 3 * cm, 3 * cm, 3 * cm])
    table.setStyle(TableStyle([
      ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
      ('BOX', (0,0), (-1,-1), 0.25, colors.black)]
    ))
    table.wrapOn(c, width, height)
    table.drawOn(c, 30, high)
    c.showPage()

    #GUARDAR PDF
    c.save()
    #OBTIENE LOS VALORES DEL BUFFER Y LOS ESCRIBE
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
 