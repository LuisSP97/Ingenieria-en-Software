from django.db import models

# Create your models here.

class Cliente(models.Model):
    rut = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=32)
    apellido = models.CharField(max_length=32)
    correo = models.CharField(max_length=32)
    telefono = models.CharField(max_length=16) # soporte para '+' (+569...)
    direccion = models.CharField(max_length=64)
    def __str__(self):
        return (str(self.rut) + " - " + self.nombre + " " + self.apellido)


class Estado(models.Model):
    # id automatico
    descripcion = models.CharField(max_length=32)
    def __str__(self):
        return self.descripcion

class Catalogo(models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64)
    precio = models.IntegerField()
    descripcion = models.CharField(max_length=512)
    def __str__(self):
        return self.nombre

class Cotizacion(models.Model):
    numero_cotizacion = models.AutoField(primary_key=True)
    rut_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    emision = models.DateTimeField('Fecha emision')
    expiracion = models.DateTimeField('Fecha expiracion')
    total = models.IntegerField()
    precio_servicio = models.IntegerField()
    estado = models.ForeignKey(Estado, on_delete = models.CASCADE)
    productos = models.ManyToManyField(Catalogo, through='Prod_Cotizacion')
    def __str__(self):
        return (str(self.rut_cliente) + ", Numero: " + str(self.numero_cotizacion)) 


class Prod_Cotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)
    codigoProducto = models.ForeignKey(Catalogo, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

class Venta(models.Model):
    numero_venta = models.AutoField(primary_key=True)
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)
    fechaEmision = models.DateTimeField('Fecha emision')
    def __str__(self):
        return self.numero_venta

