# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-07 18:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mantPlanta', '0027_auto_20170407_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='fecha',
            field=models.DateField(blank=True, null=True),
        ),
    ]
