# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-06 11:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert', '0028_auto_20180227_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='sensorparameter',
            name='parameter_name_userdef',
            field=models.CharField(default='Parameter', max_length=100),
        ),
    ]
