from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Thing
from .models import ThingEvent
from .models import ThingUser


class ThingUserInline(admin.TabularInline):
    model = ThingUser


class ThingResource(resources.ModelResource):

    class Meta:
        model = Thing
        fields = (
            "slug",
            "token",
        )


@admin.register(Thing)
class ThingAdmin(ImportExportModelAdmin):
    list_filter = [
        'slug',
    ]
    list_display = [
        'slug',
    ]
    inlines = [
        ThingUserInline,
    ]
    resource_classes = [ThingResource]


class ThingUserResource(resources.ModelResource):

    class Meta:
        model = ThingUser
        fields = (
            'thing__slug',
            'user__username',
            'created_at',
            'best_before',
        )


@admin.register(ThingUser)
class ThingUserAdmin(ImportExportModelAdmin):
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
    resource_classes = [ThingUserResource]


class ThingEventResource(resources.ModelResource):

    class Meta:
        model = ThingEvent
        fields = (
            'thing__slug',
            'user__username',
            'kind',
            'created_at',
            'usage_seconds',
        )


@admin.register(ThingEvent)
class ThingEventAdmin(ImportExportModelAdmin):
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
    resource_classes = [ThingEventResource]
