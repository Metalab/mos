from decimal import Decimal

from django.conf import settings
from django.db import migrations
from django.db import models

import members.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankCollectionMode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('num_month', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('on_intern_list', models.BooleanField(default=True)),
                ('intern_list_email', models.EmailField(max_length=254, blank=True)),
                ('street', models.CharField(max_length=200)),
                ('postcode', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=32, blank=True)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('wiki_name', models.CharField(max_length=50, null=True, blank=True)),
                ('image', models.ImageField(upload_to=members.models.get_image_path, blank=True)),
                ('last_email_ok', models.NullBooleanField()),
                ('has_active_key', models.BooleanField(default=False)),
                ('has_lazzzor_privileges', models.BooleanField(default=False)),
                ('key_id', models.CharField(max_length=100, null=True, blank=True)),
                ('lazzzor_rate', models.DecimalField(default='1.00', max_digits=3, decimal_places=2, choices=[(Decimal('1.00'), 'Standard Rate (1.00)'), (Decimal('0.50'), "Backer's Rate (0.50)")])),
                ('remark', models.TextField(null=True, blank=True)),
                ('user', models.OneToOneField(
                    to=settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE,
                )),
            ],
        ),
        migrations.CreateModel(
            name='KindOfMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='MembershipFee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateField()),
                ('end', models.DateField(null=True, blank=True)),
                ('amount', models.IntegerField()),
                ('kind_of_membership', models.ForeignKey(
                    to='members.KindOfMembership',
                    on_delete=models.CASCADE,
                )),
            ],
        ),
        migrations.CreateModel(
            name='MembershipPeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('begin', models.DateField()),
                ('end', models.DateField(null=True, blank=True)),
                ('kind_of_membership', models.ForeignKey(
                    to='members.KindOfMembership',
                    on_delete=models.CASCADE,
                )),
                ('user', models.ForeignKey(
                    to=settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE,
                )),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField()),
                ('comment', models.CharField(max_length=200, blank=True)),
                ('date', models.DateField()),
                ('original_line', models.TextField(blank=True)),
                ('original_file', models.CharField(max_length=200, null=True)),
                ('original_lineno', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='PaymentInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bank_collection_allowed', models.BooleanField(default=False)),
                ('bank_account_owner', models.CharField(max_length=200, blank=True)),
                ('bank_account_number', models.CharField(max_length=20, blank=True)),
                ('bank_name', models.CharField(max_length=100, blank=True)),
                ('bank_code', models.CharField(max_length=20, blank=True)),
                ('bank_account_iban', models.CharField(max_length=34, blank=True)),
                ('bank_account_bic', models.CharField(max_length=11, blank=True)),
                ('bank_account_mandate_reference', models.CharField(max_length=35, blank=True)),
                ('bank_account_date_of_signing', models.DateField(null=True, blank=True)),
                ('bank_collection_mode', models.ForeignKey(
                    to='members.BankCollectionMode',
                    on_delete=models.CASCADE,
                )),
                ('user', models.OneToOneField(
                    to=settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE,
                )),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='method',
            field=models.ForeignKey(
                to='members.PaymentMethod',
                on_delete=models.CASCADE,
            ),
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
                null=True,
            ),
        ),
    ]
