# Generated by Django 3.2.6 on 2021-08-20 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto_web_python_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='longitud',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
