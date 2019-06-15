from aplicacion.models import *

from django.utils import timezone



#cotizacion=Cotizacion
#
#cotizacion.rut_cliente=cliente
#cotizacion.tipo_servicio = Servicio.objects.get(pk=1)
#
#cotizacion.emision = timezone.now()
#cotizacion.expiracion = timezone.now()
#
#cotizacion.total = 120000
#
#cotizacion.precio_servicio = 30000
#
#cotizacion.estado = Estado.objects.get(pk=1)


#cotizacion = Cotizacion.objects.create( rut_cliente=Cliente.objects.get(pk=1234),
#                                        tipo_servicio = Servicio.objects.get(pk=1),
#                                        emision = timezone.now(),
#                                        expiracion = timezone.now(),
#                                        total = 120000,
#                                        precio_servicio = 30000,
#                                        estado = Estado.objects.get(pk=1))



cotizacion = Cotizacion.objects.get(pk=2)

producto = Catalogo.objects.get(pk=1)

relacion = Prod_Cotizacion(cotizacion = cotizacion, codigoProducto = producto, cantidad = 20)

relacion.save()