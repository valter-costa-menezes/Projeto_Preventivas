from django.db import migrations, models

def adicionar_pecas_predefinidas(apps, schema_editor):
    Pecas = apps.get_model('maquinas', 'Pecas')
    pecas_predefinidas = [
        {'nome': 'FILTRO DE OLEO'},
        {'nome': 'FILTRO DE AR'},
        {'nome': 'FILTRO GLP'},
        {'nome': 'OLEO MOTOR'},
        {'nome': 'OLEO HIDRAULICO'},
        {'nome': 'FILTRO HIDRAULICO'},
        {'nome': 'FILTRO RETORNO'},
        {'nome': 'CORREIA DENTADA'},
        {'nome': 'TENSOR DA CORREIA DENTADA'},
        {'nome': 'CORREIA ALTERNADOR'},
        {'nome': 'TENSOR DA CORREIA ALTERNADOR'},
        
    ]
    for peca_data in pecas_predefinidas:
        Pecas.objects.create(**peca_data)

class Migration(migrations.Migration):

    dependencies = [
        ('maquinas', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(adicionar_pecas_predefinidas),
    ]
