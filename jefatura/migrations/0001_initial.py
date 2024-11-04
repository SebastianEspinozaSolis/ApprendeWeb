# Generated by Django 5.1.2 on 2024-11-04 22:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('curso', '0001_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jefatura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curso', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='curso.curso')),
                ('profesor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='usuarios.profesor')),
            ],
        ),
    ]
