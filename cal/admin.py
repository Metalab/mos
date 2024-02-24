from django.contrib import admin

from .models import Category
from .models import Event
from .models import Location

admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Location)
