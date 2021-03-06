# Generated by Django 2.0.1 on 2018-03-02 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addwords', '0006_auto_20180302_1959'),
        ('quiz', '0020_exkkv_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExPPV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.PositiveIntegerField(blank=True, null=True)),
                ('czech', models.CharField(max_length=120)),
                ('german', models.CharField(max_length=120)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='addwords.Verb')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
