from django.contrib import admin

from .models import Thing
from .models import ThingUser


class ThingUserInline(admin.TabularInline):
    model = ThingUser


@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    list_filter = [
        'slug',
        'name',
    ]
    list_display = [
        'slug',
        'name',
    ]
    inlines = [
        ThingUserInline,
    ]