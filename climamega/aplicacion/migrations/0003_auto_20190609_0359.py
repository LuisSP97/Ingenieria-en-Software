# Generated by Django 2.2 on 2019-06-09 03:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0002_cotizacion_listaproductos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cotizacion',
            old_name='listaProductos',
            new_name='productos',
        ),
    ]
