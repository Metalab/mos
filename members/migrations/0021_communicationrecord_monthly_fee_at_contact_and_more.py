# Generated by Django 4.2.18 on 2025-02-01 22:37

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0020_communicationrecord"),
    ]

    operations = [
        migrations.AddField(
            model_name="communicationrecord",
            name="monthly_fee_at_contact",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="communicationrecord",
            name="outstanding_fees_at_contact",
            field=models.IntegerField(null=True),
        ),
    ]
