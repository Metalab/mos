# Generated by Django 3.2.20 on 2024-02-24 17:34

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0006_thingevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thingevent',
            name='usage_seconds',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
