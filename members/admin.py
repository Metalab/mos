from re import template
from typing import Optional
from datetime import datetime
import csv
from django.http.request import HttpRequest


import sepaxml
from django.forms.models import model_to_dict
from django.contrib import admin
from django.db import transaction
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import OuterRef
from django.db.models import Subquery
from django.http import HttpResponse
from django.contrib.auth.admin import UserAdmin
from django.template.loader import get_template
from django.conf import settings
from django.contrib import messages

from .models import BankCollectionMode, ContactInfo, KindOfMembership
from .models import Locker, MailinglistMail, MembershipFee, MembershipPeriod
from .models import Payment, PaymentInfo, PendingPayment, Recievable


from .views import generate_sepa, SepaException

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

class LockerInline(admin.TabularInline):
    model = Locker
    fields = ('name', 'price', 'comment')
    readonly_fields = fields

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_filter = ['user']
    list_display = ['date', 'method', 'user', 'amount', 'original_file', 'original_line']
    list_display_links = None


@admin.action(description="Make into real payments")
@transaction.atomic()
def make_into_real_payments(modeladmin, request, queryset):
    count = queryset.count()
    fields = [
        "amount",
        "comment",
        "date",
        "method_id",
        "user_id",
        "original_file",
    ]

    for pendingpayment in queryset:
        Payment.objects.create(
            **{
                f: getattr(pendingpayment, f)
                for f in fields
            }
        )
        pendingpayment.delete()

    messages.success(request, f"created {count} payments")


@admin.action(description="Generate SEPA XML for members (is active & has debt & allows monthly bank collection)")
@transaction.atomic()
def make_sepa_xml_for_members(modeladmin, request, queryset):
    queryset = queryset.filter(paymentinfo__bank_collection_allowed=True)
    queryset = queryset.filter(paymentinfo__bank_collection_mode__id=4)
    dt = datetime.now()
    # active members only
    queryset = queryset.filter(Q(membershipperiod__begin__lte=dt), Q(membershipperiod__end__isnull=True) | Q(membershipperiod__end__gte=dt))
    queryset = queryset.distinct()

    PendingPayment.objects.all().delete()

    try:
        sepa, sepaxml_filename = generate_sepa(request.user, queryset)
    except SepaException as ex:
        messages.error(request, str(ex))
        return

    try:
        sepa_export = sepa.export()
    except sepaxml.validation.ValidationError as ex:
        messages.error(request, str(ex) + ": " + str(ex.__cause__))
        return

    response = HttpResponse(sepa_export, content_type='application/xml; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{sepaxml_filename}"'
    return response



@admin.action(description="Export selected Members as csv")
@transaction.atomic()
def export_as_csv(self, request, queryset):
    field_names = ['username', 'email', 'first_name', 'last_name']

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=output.csv'
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response



@admin.register(PendingPayment)
class PendingPaymentAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_filter = ['user']
    list_display = ['date', 'method', 'user', 'amount']
    list_display_links = None
    actions = [
        make_into_real_payments,
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


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

admin.site.register(Recievable)
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

class BankCollectionModeListFilter(admin.SimpleListFilter):
    title = "bank collection mode"
    parameter_name = "bank collection mode"

    def lookups(self, request, model_admin):
        return [*BankCollectionMode.objects.all().values_list("pk", "name"), ("not_monthly", "nicht monatlich")]

    def queryset(self, request, qs):
        if self.value():
            if self.value() == "not_monthly":
                qs = qs.exclude(paymentinfo__bank_collection_mode__pk=4)
            else:
                qs = qs.filter(paymentinfo__bank_collection_mode__pk=int(self.value()))
        return qs


class MembershipPeriodListFilter(admin.SimpleListFilter):
    title = "active period"
    parameter_name = "period_kind_name"

    def lookups(self, request, model_admin):
        return [("any", "(ist aktiv)"), ("spind", "(zahlt für spind)"), *KindOfMembership.objects.all().values_list("pk", "name")]

    def queryset(self, request, qs):
        if self.value():
            dt = datetime.now()
            memberships = MembershipPeriod.objects\
                .filter(user=OuterRef('pk'))\
                .filter(Q(begin__lte=dt), Q(end__isnull=True) | Q(end__gte=dt))\
                .order_by('-begin')\
                .values("kind_of_membership__pk")
            qs = qs.annotate(active_membershipperiod_pk=Subquery(memberships[:1]))
            if self.value() == "any":
                qs = qs.filter(active_membershipperiod_pk__isnull=False)
            elif self.value() == "spind":
                spind_kinds = KindOfMembership.objects.filter(name__icontains="spind").values_list("pk", flat=True)
                qs = qs.filter(active_membershipperiod_pk__in=spind_kinds)
            else:
                qs = qs.filter(active_membershipperiod_pk=int(self.value()))
        return qs


def generate_membership_recievables(self, request, queryset):
    for user in queryset.all():
        if hasattr(user, 'contactinfo'):
            for debt in user.contactinfo.get_membership_fees():
                if not user.recievables.filter(description='Membership Fee', due_date = debt[0]).exists():
                    rec = Recievable()
                    rec.due_date = debt[0]
                    rec.amount = debt[1]
                    rec.description = 'Membership Fee'
                    rec.member = user
                    rec.save()

@admin.register(User)
class MemberAdmin(UserAdmin):
    inlines = [ContactInfoInline, PaymentInfoInline, MembershipPeriodInline,
               PaymentInline, LockerInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',
                    'is_active')
    list_filter = (
        'is_staff',
        'is_superuser',
        BankCollectionModeListFilter,
        'paymentinfo__bank_collection_allowed',
        MembershipPeriodListFilter,
        )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    actions = [send_welcome_mail, make_sepa_xml_for_members, export_as_csv, generate_membership_recievables]
    # allow to select/deselect for more members during actions
    list_max_show_all = 9999999


@admin.register(Locker)
class LockerAdmin(admin.ModelAdmin):
    list_filter = ['rented_by']
    list_display = ['name', 'rented_by', 'price']
