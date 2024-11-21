# Generated by Django 5.1.3 on 2024-11-21 20:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asistencia', '0002_asistencia_justificacion_alter_asistencia_alumno_and_more'),
        ('usuarios', '0002_alter_perfil_rut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistencia',
            name='alumno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asistencias', to='usuarios.alumno'),
        ),
    ]