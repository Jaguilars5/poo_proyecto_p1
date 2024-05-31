# Generated by Django 4.2 on 2024-05-31 12:22

import datetime
import django.core.validators
from django.db import migrations, models
import proy_sales.utils


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_product_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='description',
            field=models.CharField(max_length=100, unique=True, verbose_name='Articulo'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(max_length=100, unique=True, verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=100, unique=True, verbose_name='Articulo'),
        ),
        migrations.AlterField(
            model_name='product',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 12, 22, 39, 818051, tzinfo=datetime.timezone.utc), verbose_name='Fecha Caducidad'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='phone',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='El número de teléfono debe contener entre 9 y 15 dígitos.', regex='^\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='ruc',
            field=models.CharField(max_length=13, unique=True, validators=[proy_sales.utils.valida_cedula]),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='state',
            field=models.BooleanField(default=True, verbose_name='Activo'),
        ),
    ]