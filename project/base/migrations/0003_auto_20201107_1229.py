# Generated by Django 3.1.2 on 2020-11-07 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20201107_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address_lane_1',
            field=models.CharField(max_length=200),
        ),
    ]