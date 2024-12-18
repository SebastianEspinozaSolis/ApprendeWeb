# Generated by Django 5.1.2 on 2024-11-21 19:57

import datetime
import django.core.validators
import usuarios.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_alter_perfil_rut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrador',
            name='cargo',
            field=models.CharField(default='sin definir', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='apoderado',
            name='telefono',
            field=models.CharField(default='sin contacto', max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='perfil',
            name='fecha_nacimiento',
            field=models.DateField(default=datetime.date(2000, 1, 1)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='perfil',
            name='nombre',
            field=models.CharField(default='desconocido', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='perfil',
            name='rut',
            field=models.CharField(default='10.000.000-1', max_length=12, validators=[django.core.validators.RegexValidator(code='invalid_rut', message='Formato de RUT inválido. Debe ser como 12345678-9', regex='^[0-9]{7,8}-[0-9Kk]$'), usuarios.models.validar_rut]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='perfil',
            name='segundo_rol',
            field=models.CharField(choices=[('administrador', 'Administrador'), ('profesor', 'Profesor'), ('apoderado', 'Apoderado'), ('alumno', 'Alumno')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='sexo',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], default='F', max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profesor',
            name='especialidad',
            field=models.CharField(default='sin definir', max_length=100),
            preserve_default=False,
        ),
    ]
