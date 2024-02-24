# Generated by Django 3.2.20 on 2024-02-24 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('things', '0005_auto_20240224_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThingEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('LOGIN', 'Login'), ('LOGOUT', 'Logout'), ('USAGE_MEMBER', 'Zeit (Member)'), ('USAGE_NONMEMBER', 'Zeit (Nicht-Member)')], db_index=True, max_length=32)),
                ('usage_seconds', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('thing', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='things.thing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thingevents', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]