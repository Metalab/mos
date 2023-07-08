# Generated by Django 3.2.20 on 2023-07-08 15:04

from django.db import migrations
import easy_thumbnails.fields
import members.models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_alter_contactinfo_last_email_ok'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, upload_to=members.models.get_image_path),
        ),
    ]