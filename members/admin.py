from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import Payment, PaymentInfo, MembershipPeriod, ContactInfo
from metaauth.models import UserPermission


class ContactInfoInline(admin.StackedInline):
    model = ContactInfo
    max_num = 1


class PaymentInfoInline(admin.StackedInline):
    model = PaymentInfo
    max_num = 1


class MembershipPeriodInline(admin.TabularInline):
    model = MembershipPeriod


class PermissionInline(admin.StackedInline):
    model = UserPermission
    def get_formset(self, request, obj=None, **kwargs):
        """
        Override the formset function in order to remove the add and change buttons beside the foreign key pull-down
        menus in the inline.
        """
        formset = super(PermissionInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['device'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        return formset


class PaymentInline(admin.TabularInline):
    model = Payment
    fields = ('date', 'amount', 'method')
    ordering = ('date',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_filter = ['user']
    list_display = ['date', 'method', 'user', 'amount', 'original_file', 'original_line']
    list_display_links = None


admin.site.unregister(User)


@admin.register(User)
class MemberAdmin(UserAdmin):
    inlines = [ContactInfoInline, PaymentInfoInline, PermissionInline,
               MembershipPeriodInline, PaymentInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',
                    'is_active')
    list_filter = ('is_staff', 'is_superuser', 'paymentinfo__bank_collection_mode')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
