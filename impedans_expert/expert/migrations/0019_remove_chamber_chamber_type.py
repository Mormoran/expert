# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-02-16 13:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expert', '0018_auto_20180216_1129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chamber',
            name='chamber_type',
        ),
    ]
