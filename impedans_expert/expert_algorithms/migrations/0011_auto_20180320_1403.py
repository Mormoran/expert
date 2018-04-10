# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-20 14:03
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('expert_algorithms', '0010_auto_20180315_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='algorithmsettings',
            name='configuration_thread',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='streamalgorithm',
            unique_together=set([('algorithm_name',)]),
        ),
    ]
