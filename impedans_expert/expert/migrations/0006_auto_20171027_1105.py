# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-27 11:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expert', '0005_auto_20171027_1036'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='data',
            unique_together=set([('time', 'sensor', 'parameter', 'parameter_value')]),
        ),
    ]
