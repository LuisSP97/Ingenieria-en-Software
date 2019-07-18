# Generated by Django 2.2 on 2019-07-18 19:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='fechaEmision',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha emision'),
            preserve_default=False,
        ),
    ]