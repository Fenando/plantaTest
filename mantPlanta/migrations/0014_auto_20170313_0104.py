# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-13 01:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mantPlanta', '0013_auto_20170313_0053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informacion',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='mantPlanta/static/imagenes/'),
        ),
    ]
