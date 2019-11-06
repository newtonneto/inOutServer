# Generated by Django 2.2.5 on 2019-11-06 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inout', '0004_auto_20191106_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgao',
            name='estado',
            field=models.IntegerField(choices=[(1, 'Acre (AC)'), (2, 'Alagoas (AL)'), (3, 'Amapá (AP)'), (4, 'Amazonas (AM)'), (5, 'Bahia (BA)'), (6, 'Ceará (CE)'), (7, 'Distrito Federal (DF)'), (8, 'Espírito Santo (ES)'), (9, 'Goiás (GO)'), (10, 'Maranhão (MA)'), (11, 'Mato Grosso (MT)'), (12, 'Mato Grosso do Sul (MS)'), (13, 'Minas Gerais (MG)'), (14, 'Pará (PA)'), (15, 'Paraíba (PB)'), (16, 'Paraná (PR)'), (17, 'Pernambuco (PE)'), (18, 'Piauí (PI)'), (19, 'Rio de Janeiro (RJ)'), (20, 'Rio Grande do Norte (RN)'), (21, 'Rio Grande do Sul (RS)'), (22, 'Rondônia (RO)'), (23, 'Roraima (RR)'), (24, 'Santa Catarina (SC)'), (25, 'São Paulo (SP)'), (26, 'Sergipe (SE)'), (27, 'Tocantins (TO)')], default=20),
            preserve_default=False,
        ),
    ]
