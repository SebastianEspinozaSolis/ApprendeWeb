# Generated by Django 5.1.2 on 2024-11-21 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_alter_administrador_cargo_alter_apoderado_telefono_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True),
        ),
    ]
