# Generated by Django 2.2.3 on 2019-11-24 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inout', '0006_auto_20191124_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgao',
            name='ativo',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='setor',
            name='ativo',
            field=models.BooleanField(),
        ),
    ]