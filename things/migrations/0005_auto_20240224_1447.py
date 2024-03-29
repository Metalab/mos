# Generated by Django 3.2.20 on 2024-02-24 14:47

from django.db import migrations
from django.db import models

import things.models


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0004_remove_thing_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thing',
            name='slug',
            field=models.SlugField(help_text="Name of the thing, e.g. 'laser'", unique=True),
        ),
        migrations.AlterField(
            model_name='thing',
            name='token',
            field=models.CharField(default=things.models.make_token, help_text='auto generated, allows the machine to get the key IDs, KEEP SECRET', max_length=128),
        ),
    ]
