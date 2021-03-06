# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-02-27 16:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expert', '0027_auto_20180222_1233'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter_name_userdef', models.CharField(default="Parameter", max_length=100)),
                ('live_value', models.FloatField()),
                ('parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert.Parameter')),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert.Sensor')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='sensorparameter',
            unique_together=set([('sensor', 'parameter_name_userdef')]),
        ),
    ]
