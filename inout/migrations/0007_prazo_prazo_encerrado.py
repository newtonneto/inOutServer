# Generated by Django 2.2.3 on 2019-09-22 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inout', '0006_remove_prazo_status_do_prazo'),
    ]

    operations = [
        migrations.AddField(
            model_name='prazo',
            name='prazo_encerrado',
            field=models.BooleanField(default=False),
        ),
    ]
