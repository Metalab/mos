# Generated by Django 4.2.18 on 2025-02-01 22:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("members", "0019_pendingpayment_creator"),
    ]

    operations = [
        migrations.CreateModel(
            name="CommunicationRecord",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("contacted_on", models.DateField()),
                ("initial_contact", models.BooleanField(default=False)),
                (
                    "contacted_by",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("contact_resolved", models.BooleanField(default=False)),
                ("comment", models.CharField(blank=True, max_length=1000, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
