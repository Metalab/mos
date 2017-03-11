# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import members.models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=members.models.get_image_path, blank=True),
        ),
    ]
