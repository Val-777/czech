# Generated by Django 2.0.1 on 2018-02-28 16:17

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0019_auto_20180130_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='exkkv',
            name='options',
            field=jsonfield.fields.JSONField(blank=True, default=dict),
        ),
    ]