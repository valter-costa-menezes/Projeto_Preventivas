# Generated by Django 5.0.7 on 2024-07-18 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patrimonio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frota', models.CharField(max_length=6, verbose_name='Número de frota')),
                ('horimetro', models.IntegerField(verbose_name='Horimetro de máquina')),
            ],
        ),
    ]
