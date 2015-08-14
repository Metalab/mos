from __future__ import absolute_import

from django.contrib import admin

from .models import Event, Category, Location


admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Location)
