# Generated by Django 3.2.20 on 2023-07-08 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_pendingpayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingpayment',
            name='original_file',
            field=models.CharField(max_length=200, null=True),
        ),
    ]