# Generated by Django 5.0.7 on 2024-07-20 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maquinas', '0005_alter_ultimapreventiva_horadepreventiva_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ultimapreventiva',
            name='HoradePreventiva',
            field=models.IntegerField(default=None, verbose_name='Preventiva de quantas horas'),
        ),
        migrations.AlterField(
            model_name='ultimapreventiva',
            name='OS',
            field=models.IntegerField(default=None, verbose_name='Ordem de serviço'),
        ),
        migrations.AlterField(
            model_name='ultimapreventiva',
            name='frota',
            field=models.IntegerField(default=None, verbose_name='Número de frota'),
        ),
        migrations.AlterField(
            model_name='ultimapreventiva',
            name='horimetro',
            field=models.IntegerField(default=None, verbose_name='Horimetro de máquina'),
        ),
    ]
