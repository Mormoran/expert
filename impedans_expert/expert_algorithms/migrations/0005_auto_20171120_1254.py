# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-20 12:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expert_algorithms', '0004_auto_20171120_1247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='algorithmrunresults',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='algorithmstate',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='algorithmtimeresults',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='goldenset',
            name='owner',
        ),
    ]
