# Generated by Django 2.2.3 on 2019-11-24 17:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data_de_recebimento', models.DateField()),
                ('tipo', models.IntegerField(choices=[(1, 'Carta'), (2, 'Convite'), (3, 'Documento'), (4, 'Email'), (5, 'Mandado de Intimação'), (6, 'Memorando'), (7, 'Memorando Circular'), (8, 'Movimentação da Solicitação'), (9, 'Notificação'), (10, 'Ofício'), (11, 'Ofício Circular'), (12, 'Requerimento'), (13, 'Outro')], default=10)),
                ('numero', models.CharField(max_length=30)),
                ('emissor', models.CharField(max_length=50)),
                ('assunto', models.CharField(max_length=1000)),
                ('despacho', models.CharField(max_length=200)),
                ('entrega_pessoal', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'documento',
            },
        ),
        migrations.CreateModel(
            name='Livro',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('tipo', models.IntegerField(choices=[(1, 'Externo'), (2, 'Interno'), (3, 'USF')], default=2)),
                ('ano', models.IntegerField()),
                ('volume', models.IntegerField()),
                ('encerrado', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'livro',
            },
        ),
        migrations.CreateModel(
            name='Orgao',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=50)),
                ('sigla', models.CharField(max_length=10)),
                ('esfera', models.IntegerField(choices=[(1, 'Estadual'), (2, 'Federal'), (3, 'Municipal')])),
                ('estado', models.IntegerField(choices=[(1, 'Acre (AC)'), (2, 'Alagoas (AL)'), (3, 'Amapá (AP)'), (4, 'Amazonas (AM)'), (5, 'Bahia (BA)'), (6, 'Ceará (CE)'), (7, 'Distrito Federal (DF)'), (8, 'Espírito Santo (ES)'), (9, 'Goiás (GO)'), (10, 'Maranhão (MA)'), (11, 'Mato Grosso (MT)'), (12, 'Mato Grosso do Sul (MS)'), (13, 'Minas Gerais (MG)'), (14, 'Pará (PA)'), (15, 'Paraíba (PB)'), (16, 'Paraná (PR)'), (17, 'Pernambuco (PE)'), (18, 'Piauí (PI)'), (19, 'Rio de Janeiro (RJ)'), (20, 'Rio Grande do Norte (RN)'), (21, 'Rio Grande do Sul (RS)'), (22, 'Rondônia (RO)'), (23, 'Roraima (RR)'), (24, 'Santa Catarina (SC)'), (25, 'São Paulo (SP)'), (26, 'Sergipe (SE)'), (27, 'Tocantins (TO)')], default=20)),
                ('municipio', models.CharField(max_length=32)),
                ('ativo', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'orgao',
            },
        ),
        migrations.CreateModel(
            name='Pagina',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('numero', models.IntegerField()),
                ('fk_livro', models.ForeignKey(db_column='fk_livro', on_delete=django.db.models.deletion.DO_NOTHING, to='inout.Livro')),
            ],
            options={
                'db_table': 'pagina',
            },
        ),
        migrations.CreateModel(
            name='Processo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('numero', models.CharField(max_length=21)),
            ],
            options={
                'db_table': 'processo',
            },
        ),
        migrations.CreateModel(
            name='Setor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=50)),
                ('sigla', models.CharField(max_length=10)),
                ('ativo', models.IntegerField(default=1)),
                ('fk_orgao', models.ForeignKey(db_column='fk_orgao', on_delete=django.db.models.deletion.DO_NOTHING, to='inout.Orgao')),
            ],
            options={
                'db_table': 'setor',
            },
        ),
        migrations.CreateModel(
            name='Protocolo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('entregue', models.IntegerField()),
                ('data_da_entrega', models.DateField(blank=True, null=True)),
                ('fk_documento', models.ForeignKey(db_column='fk_documento', on_delete=django.db.models.deletion.DO_NOTHING, to='inout.Documento')),
                ('fk_pagina', models.ForeignKey(db_column='fk_pagina', on_delete=django.db.models.deletion.DO_NOTHING, to='inout.Pagina')),
                ('fk_setor_destino', models.ForeignKey(db_column='fk_setor_destino', on_delete=django.db.models.deletion.DO_NOTHING, related_name='setor_de_destino', to='inout.Setor')),
                ('fk_setor_origem', models.ForeignKey(db_column='fk_setor_origem', on_delete=django.db.models.deletion.DO_NOTHING, related_name='setor_de_origem', to='inout.Setor')),
            ],
            options={
                'db_table': 'protocolo',
            },
        ),
        migrations.CreateModel(
            name='Prazo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.IntegerField()),
                ('vencimento', models.DateField()),
                ('encerrado', models.IntegerField(blank=True, null=True)),
                ('dilacao', models.IntegerField(blank=True, null=True)),
                ('quantidade_de_dilacoes', models.IntegerField(blank=True, null=True)),
                ('fk_documento', models.ForeignKey(db_column='fk_documento', on_delete=django.db.models.deletion.DO_NOTHING, to='inout.Documento')),
            ],
            options={
                'db_table': 'prazo',
            },
        ),
        migrations.CreateModel(
            name='Lotacao',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('cargo', models.IntegerField(choices=[(1, 'Arquiteto'), (2, 'Assistente Administrativo'), (3, 'Chefe de Gabinete'), (4, 'Diretor'), (5, 'Estagiário'), (6, 'Fiscal'), (7, 'Recepcionista'), (8, 'Secretário'), (9, 'Técnico em Informática')])),
                ('entrada', models.DateField()),
                ('saida', models.DateField(blank=True, null=True)),
                ('fk_setor', models.ForeignKey(db_column='fk_setor', on_delete=django.db.models.deletion.DO_NOTHING, to='inout.Setor')),
                ('fk_user', models.ForeignKey(db_column='fk_user', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'lotacao',
            },
        ),
        migrations.AddField(
            model_name='livro',
            name='fk_setor',
            field=models.ForeignKey(db_column='fk_setor', on_delete=django.db.models.deletion.DO_NOTHING, to='inout.Setor'),
        ),
        migrations.AddField(
            model_name='documento',
            name='fk_processo',
            field=models.ForeignKey(blank=True, db_column='fk_processo', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inout.Processo'),
        ),
        migrations.AddField(
            model_name='documento',
            name='fk_user',
            field=models.ForeignKey(db_column='fk_user', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
