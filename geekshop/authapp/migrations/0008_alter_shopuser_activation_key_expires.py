# Generated by Django 3.2.5 on 2022-01-21 20:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0007_auto_20220118_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 23, 20, 49, 58, 542277)),
        ),
    ]