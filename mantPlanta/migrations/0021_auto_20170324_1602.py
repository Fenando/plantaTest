# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-24 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mantPlanta', '0020_area_planta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informacion',
            name='info',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
