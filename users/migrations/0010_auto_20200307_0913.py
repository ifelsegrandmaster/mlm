# Generated by Django 3.0.2 on 2020-03-07 09:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20200129_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2020, 3, 7, 9, 13, 29, 630045)),
        ),
    ]
