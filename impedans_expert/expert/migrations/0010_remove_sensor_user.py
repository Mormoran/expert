# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-14 23:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expert', '0009_auto_20171114_1027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensor',
            name='user',
        ),
    ]
