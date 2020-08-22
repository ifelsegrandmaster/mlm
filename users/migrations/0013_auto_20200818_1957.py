# Generated by Django 3.0.5 on 2020-08-18 19:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20200816_1817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_child_of',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_grand_child_of',
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
