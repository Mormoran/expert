# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-15 15:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expert', '0031_recipe_description'),
        ('expert_algorithms', '0009_auto_20180219_1150'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlgorithmSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('configuration_thread', models.CharField(max_length=255)),
                ('date_time', models.DateTimeField(default=datetime.datetime.now)),
                ('result_name', models.CharField(max_length=255)),
                ('start', models.IntegerField()),
                ('stop', models.IntegerField()),
                ('parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert.Parameter')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='AlgorithmVariables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('algorithm_config_setup', models.CharField(max_length=500)),
                ('algorithm_configuration', models.CharField(max_length=500)),
                ('date_time', models.DateTimeField(default=datetime.datetime.now)),
                ('ready', models.BooleanField(default=False)),
                ('algorithm_settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert_algorithms.AlgorithmSettings')),
                ('chamber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert.Chamber')),
            ],
        ),
        migrations.CreateModel(
            name='StreamAlgorithm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algorithm_name', models.CharField(max_length=50, unique=True)),
                ('algorithm_description', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='algorithmsettings',
            name='stream_algorithm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert_algorithms.StreamAlgorithm'),
        ),
    ]
