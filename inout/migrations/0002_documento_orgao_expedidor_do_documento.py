# Generated by Django 2.2.3 on 2019-08-25 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inout', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='orgao_expedidor_do_documento',
            field=models.CharField(default=0, max_length=150),
            preserve_default=False,
        ),
    ]