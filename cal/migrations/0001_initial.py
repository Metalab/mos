import datetime

from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('teaser', models.TextField(max_length=200, null=True, blank=True)),
                ('wikiPage', models.CharField(max_length=200)),
                ('startDate', models.DateTimeField()),
                ('endDate', models.DateTimeField(null=True, blank=True)),
                ('who', models.CharField(max_length=200, blank=True)),
                ('where', models.CharField(max_length=200, blank=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('deleted', models.BooleanField(default=False)),
                ('category', models.ForeignKey(
                    blank=True,
                    on_delete=models.CASCADE,
                    to='core.Category',
                    null=True,
                )),
                ('created_by', models.ForeignKey(
                    to=settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE,
                )),
                ('location', models.ForeignKey(
                    blank=True,
                    to='core.Location',
                    on_delete=models.CASCADE,
                    null=True,
                )),
            ],
        ),
    ]
