# Generated by Django 3.2.20 on 2024-02-24 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0003_auto_20240224_1415'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thing',
            name='name',
        ),
    ]
