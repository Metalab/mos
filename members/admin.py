from __future__ import unicode_literals
from re import template

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.template.loader import get_template
from django.conf import settings
from django.contrib import messages

from .models import Payment, PaymentInfo, MembershipPeriod, ContactInfo, KindOfMembership, MembershipFee, BankCollectionMode, MailinglistMail


class ContactInfoInline(admin.StackedInline):
    model = ContactInfo
    max_num = 1


class PaymentInfoInline(admin.StackedInline):
    model = PaymentInfo
    max_num = 1


class MembershipPeriodInline(admin.TabularInline):
    model = MembershipPeriod


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

class MembershipFeeInline(admin.TabularInline):
    model = MembershipFee
    ordering = ('start',)

@admin.register(KindOfMembership)
class KindOfMembershipAdmin(admin.ModelAdmin):
    inlines = [MembershipFeeInline]

@admin.register(BankCollectionMode)
class BankCollectionModeAdmin(admin.ModelAdmin):
    pass


@admin.register(MailinglistMail)
class MemberAdmin(admin.ModelAdmin):
    search_fields = (
        'email',
    )
    list_display = (
        'email',
        'on_intern_list',
    )


admin.site.unregister(User)


@admin.action(description='Send welcome mail')
def send_welcome_mail(modeladmin, request, queryset):
    tpl_subject = get_template("members/new_member_welcome.mail.subject")
    tpl_body = get_template("members/new_member_welcome.mail")

    for user in queryset.all():
        ctx = {
            "user": user,
        }
        user.contactinfo.send_mail(
            tpl_subject.render(ctx).strip(),
            tpl_body.render(ctx),
            settings.HOS_EMAIL_LOG,
        )

    messages.success(request, 'Welcome mail sent.')


@admin.register(User)
class MemberAdmin(UserAdmin):
    inlines = [ContactInfoInline, PaymentInfoInline, MembershipPeriodInline,
               PaymentInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',
                    'is_active')
    list_filter = ('is_staff', 'is_superuser', 'paymentinfo__bank_collection_mode')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    actions = [send_welcome_mail]
