# Generated by Django 2.2.3 on 2019-09-19 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inout', '0003_auto_20190826_2157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_de_usuario', models.CharField(max_length=20)),
                ('senha', models.CharField(max_length=16)),
            ],
        ),
    ]