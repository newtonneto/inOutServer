# Generated by Django 2.2.6 on 2019-11-07 18:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inout', '0005_orgao_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lotacao',
            name='entrada',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 7, 18, 55, 45, 786674, tzinfo=utc), verbose_name='Data de entrada na função'),
        ),
        migrations.AlterField(
            model_name='setor',
            name='nome',
            field=models.CharField(max_length=50),
        ),
    ]
