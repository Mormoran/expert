# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-02-19 11:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expert_import', '0009_auto_20180219_1150'),
        ('expert_algorithms', '0008_auto_20180219_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='algorithmrunresult',
            name='run',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='expert_import.Run'),
        ),
        migrations.AlterUniqueTogether(
            name='algorithmrunresult',
            unique_together=set([('algorithm_run', 'parameter', 'value')]),
        ),
    ]
