# Generated by Django 2.2 on 2019-06-09 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cotizacion',
            name='listaProductos',
            field=models.ManyToManyField(through='aplicacion.Prod_Cotizacion', to='aplicacion.Catalogo'),
        ),
    ]