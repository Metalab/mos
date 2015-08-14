# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('teaser', models.TextField(max_length=200, null=True, blank=True)),
                ('wikiPage', models.CharField(max_length=200, null=True, blank=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('finished_at', models.DateField(null=True, blank=True)),
                ('deleted', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
