# Generated by Django 2.2.3 on 2019-11-12 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inout', '0003_auto_20191112_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='entrega_pessoal',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prazo',
            name='encerrado',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prazo',
            name='vencimento',
            field=models.DateField(),
        ),
    ]
