from django.contrib import admin

from .models import Thing
from .models import ThingEvent
from .models import ThingUser


class ThingUserInline(admin.TabularInline):
    model = ThingUser


@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    list_filter = [
        'slug',
    ]
    list_display = [
        'slug',
    ]
    inlines = [
        ThingUserInline,
    ]


@admin.register(ThingUser)
class ThingUser(admin.ModelAdmin):
    list_filter = [
        'thing',
        'user',
    ]
    list_display = [
        'thing',
        'user',
        'created_at',
        'best_before',
    ]


@admin.register(ThingEvent)
class ThingEvent(admin.ModelAdmin):
    list_filter = [
        'thing',
        'user',
        'kind',
    ]
    list_display = [
        'thing',
        'user',
        'kind',
        'created_at',
    ]
