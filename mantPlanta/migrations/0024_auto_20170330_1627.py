# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-30 16:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mantPlanta', '0023_acciones'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mantencion',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='media/images/'),
        ),
    ]