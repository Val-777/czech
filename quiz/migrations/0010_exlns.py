# Generated by Django 2.0.1 on 2018-01-21 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_exaas'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExLNS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.PositiveIntegerField(blank=True, null=True)),
                ('czech', models.CharField(max_length=120, unique=True)),
                ('german', models.CharField(max_length=120)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Noun')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
