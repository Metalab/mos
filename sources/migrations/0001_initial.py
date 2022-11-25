from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WikiChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=300)),
                ('author', models.CharField(max_length=300)),
                ('updated', models.DateTimeField()),
            ],
        ),
    ]
