from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Catalogo)
admin.site.register(Cliente)
admin.site.register(Servicio)
admin.site.register(Cotizacion)
admin.site.register(Estado)
admin.site.register(Prod_Cotizacion)
admin.site.register(Venta)