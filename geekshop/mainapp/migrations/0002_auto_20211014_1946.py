# Generated by Django 3.2.5 on 2021-10-14 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
