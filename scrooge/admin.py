from django.contrib import admin

from mos.scrooge.models import Account, AccountAdmin, Product, ProductAdmin

admin.site.register(Account, AccountAdmin)
admin.site.register(Product, ProductAdmin)
