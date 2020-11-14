# Generated by Django 3.1.2 on 2020-11-09 03:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_contactsupport'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactsupport',
            name='reported_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reported_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contactsupport',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_on', to=settings.AUTH_USER_MODEL),
        ),
    ]
