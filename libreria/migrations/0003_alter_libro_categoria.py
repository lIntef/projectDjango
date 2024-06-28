# Generated by Django 5.0.6 on 2024-06-28 09:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0002_categoria_libro_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='categoria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='libros', to='libreria.categoria', verbose_name='Categoria'),
        ),
    ]