from django.db import models

from django.db import models
from django.db import connection, transaction
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import admin
from datetime import datetime

# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, null=True, blank=True)
    credentialId = models.CharField(max_length=200, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def add_booking(self, amount, comment):
        cursor = connection.cursor()
        nrAffected = cursor.execute("update scrooge_account set balance=balance+%s where id=%s and balance+%s >= 0",
            [ amount, self.id, amount])
        if (nrAffected == 0):
            return None
        transaction.commit_unless_managed()
        booking = AccountBooking.objects.create(account=self, amount=amount, description=comment)
        booking.save()
        return booking

    def __unicode__(self):
        return u'Account %s' % self.name

class Product(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=200)
    ean = models.CharField(max_length=200, unique=True)

class AccountBooking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=2000)
    

class ProductAdmin(admin.ModelAdmin):
    list_display = ('ean', 'name', 'price')
    search_fields = ('ean', 'name')
    ordering = ('name',)

class AccountBookingInline(admin.TabularInline):
    model = AccountBooking
    #fields = ('created_at', 'amount', 'description')
    ordering = ('created_at',)

class AccountAdmin(admin.ModelAdmin):
    inlines = [AccountBookingInline]
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

