# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-27 17:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_auto_20171127_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noun',
            name='artikel',
            field=models.CharField(choices=[('der', 'der'), ('die', 'die'), ('das', 'das')], max_length=3),
        ),
    ]
