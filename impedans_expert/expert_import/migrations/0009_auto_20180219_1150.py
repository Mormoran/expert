# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-02-19 11:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expert', '0020_auto_20180219_1150'),
        ('expert_algorithms', '0008_auto_20180219_1150'),
        ('expert_import', '0008_auto_20180208_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(db_index=True)),
                ('end_time', models.DateTimeField(db_index=True)),
                ('chamber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert.Chamber')),
                ('recipe', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='expert.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RunParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('param_name_user_defined', models.BooleanField(default=True)),
                ('chamber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert.Chamber')),
                ('parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert.Parameter')),
            ],
        ),
        migrations.CreateModel(
            name='RunProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_name', models.CharField(max_length=20)),
                ('property_value', models.CharField(max_length=50)),
                ('user_defined', models.BooleanField(default=True)),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert_import.Run')),
            ],
        ),
        migrations.CreateModel(
            name='RunValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('user_defined', models.BooleanField(default=True)),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert_import.Run')),
                ('run_parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert_import.RunParameter')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='runproperties',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='runproperties',
            name='runs',
        ),
        migrations.AlterUniqueTogether(
            name='runs',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='runs',
            name='chamber',
        ),
        migrations.RemoveField(
            model_name='runs',
            name='file',
        ),
        migrations.RemoveField(
            model_name='runs',
            name='recipe',
        ),
        migrations.DeleteModel(
            name='RunProperties',
        ),
        migrations.DeleteModel(
            name='Runs',
        ),
        migrations.AlterUniqueTogether(
            name='runvalue',
            unique_together=set([('run', 'value')]),
        ),
        migrations.AlterUniqueTogether(
            name='runproperty',
            unique_together=set([('property_name', 'run')]),
        ),
        migrations.AlterUniqueTogether(
            name='runparameter',
            unique_together=set([('parameter', 'chamber')]),
        ),
        migrations.AlterUniqueTogether(
            name='run',
            unique_together=set([('start_time', 'end_time', 'chamber')]),
        ),
    ]
