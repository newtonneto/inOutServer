# Generated by Django 2.2.6 on 2019-10-17 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inout', '0009_documento_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Livro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=10)),
                ('ano', models.DateTimeField(verbose_name='Ano do Livro')),
                ('volume', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Orgao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pagina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('livro', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inout.Livro')),
            ],
        ),
        migrations.CreateModel(
            name='Processo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=30)),
            ],
        ),
        migrations.RenameField(
            model_name='documento',
            old_name='assunto_do_documento',
            new_name='assunto',
        ),
        migrations.RenameField(
            model_name='documento',
            old_name='data_de_entrada',
            new_name='data_de_recebimento',
        ),
        migrations.RenameField(
            model_name='documento',
            old_name='despacho_do_documento',
            new_name='despacho',
        ),
        migrations.RenameField(
            model_name='documento',
            old_name='orgao_expedidor_do_documento',
            new_name='emissor',
        ),
        migrations.RenameField(
            model_name='documento',
            old_name='numero_do_documento',
            new_name='numero',
        ),
        migrations.RenameField(
            model_name='prazo',
            old_name='prazo_encerrado',
            new_name='encerrado',
        ),
        migrations.RenameField(
            model_name='prazo',
            old_name='tipo_de_prazo',
            new_name='tipo',
        ),
        migrations.RenameField(
            model_name='prazo',
            old_name='data_do_prazo',
            new_name='vencimento',
        ),
        migrations.RemoveField(
            model_name='documento',
            name='numero_do_processo',
        ),
        migrations.RemoveField(
            model_name='documento',
            name='tipo_de_documento',
        ),
        migrations.AddField(
            model_name='documento',
            name='tipo',
            field=models.IntegerField(choices=[(0, 'Carta'), (1, 'Convite'), (2, 'Documento'), (3, 'Email'), (4, 'Mandado de Intimação'), (5, 'Memorando'), (6, 'Memorando Circular'), (7, 'Movimentação da Solicitação'), (8, 'Notificação'), (9, 'Ofício'), (10, 'Ofício Circular'), (11, 'Requerimento'), (12, 'Outros')], default=9),
        ),
        migrations.AlterField(
            model_name='documento',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Setor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('orgao', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inout.Orgao')),
            ],
        ),
        migrations.CreateModel(
            name='Protocolo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entregue', models.BooleanField(default=False)),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inout.Documento')),
                ('pagina', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inout.Pagina')),
                ('setor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inout.Setor')),
            ],
        ),
        migrations.AddField(
            model_name='livro',
            name='setor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inout.Setor'),
        ),
        migrations.AddField(
            model_name='documento',
            name='processo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inout.Processo'),
        ),
    ]