# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-24 10:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expert_import', '0004_runs_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='runs',
            name='recipe',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='expert.Recipe'),
        ),
    ]
