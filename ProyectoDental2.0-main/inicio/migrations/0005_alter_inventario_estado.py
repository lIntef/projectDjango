# Generated by Django 5.0.6 on 2024-08-02 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0004_alter_userprofile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventario',
            name='estado',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Disponible'), (2, 'Agotado'), (3, 'Por Recibir')], default=1),
        ),
    ]
