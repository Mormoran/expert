# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-02-19 11:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expert', '0020_auto_20180219_1150'),
        ('expert_algorithms', '0007_algorithmrun_result_parameter'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlgorithmRunResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('algorithm_run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert_algorithms.AlgorithmRun')),
                ('parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert.Parameter')),
            ],
        ),
        migrations.RenameModel(
            old_name='AlgorithmTimeResults',
            new_name='AlgorithmTimeResult',
        ),
        migrations.AlterUniqueTogether(
            name='algorithmrunresults',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='algorithmrunresults',
            name='algorithm_run',
        ),
        migrations.RemoveField(
            model_name='algorithmrunresults',
            name='parameter',
        ),
        migrations.RemoveField(
            model_name='algorithmrunresults',
            name='runs',
        ),
        migrations.DeleteModel(
            name='AlgorithmRunResults',
        ),
    ]
