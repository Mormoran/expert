# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-27 11:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expert', '0015_auto_20171124_1010'),
        ('expert_algorithms', '0005_auto_20171120_1254'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='goldenset',
            unique_together=set([('step', 'chamber')]),
        ),
    ]
