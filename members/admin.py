import csv
from datetime import date
from datetime import datetime
from secrets import token_urlsafe

import sepaxml
from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import OuterRef
from django.db.models import Q
from django.db.models import Subquery
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.admin import ImportExportModelAdmin

from members.models import members_due_for_bank_collection
from things.models import ThingUser

from .models import BankCollectionMode
from .models import BankImportMatcher
from .models import CommunicationRecord
from .models import ContactInfo
from .models import KindOfMembership
from .models import Locker
from .models import MailinglistMail
from .models import MembershipFee
from .models import MembershipPeriod
from .models import Payment
from .models import PaymentInfo
from .models import PendingPayment
from .views import SepaException
from .views import generate_sepa


class ContactInfoInline(admin.StackedInline):
    model = ContactInfo
    max_num = 1


class PaymentInfoInline(admin.StackedInline):
    model = PaymentInfo
    max_num = 1


class MembershipPeriodInline(admin.TabularInline):
    model = MembershipPeriod

class CommunicationRecordInline(admin.TabularInline):
    model = CommunicationRecord


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


@admin.action(description="Generate SEPA XML for members (is active & allows bank collection & is correct month for member)")
@transaction.atomic()
def make_sepa_xml_for_members(modeladmin, request, queryset):
    queryset = members_due_for_bank_collection(queryset)
    dt = datetime.now()
    # active members only
    queryset = queryset.filter(Q(membershipperiod__begin__lte=dt), Q(membershipperiod__end__isnull=True) | Q(membershipperiod__end__gte=dt))
    queryset = queryset.distinct()

    # PendingPayment.objects.all().delete()

    if PendingPayment.objects.exists():
        messages.error(request, "Pending Payments already exist. Please check Pending Payments and convert them into actual payments or delete them as applicable.")
        return

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



@admin.action(description="Export selected members with monthly and active fees as CSV.")
@transaction.atomic()
def export_member_csv_with_fees(self, request, queryset):
    field_names = ['username', 'email', 'first_name', 'last_name']

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=output.csv'
    writer = csv.writer(response)

    column_names = field_names + ['monthly_fees', 'outstanding_fees']
    writer.writerow(column_names)

    for obj in queryset:
        cols = [getattr(obj, field) for field in field_names]
        cols.append(obj.contactinfo.get_debt_for_this_month())
        cols.append(obj.contactinfo.get_debts())
        row = writer.writerow(cols)

    return response



@admin.register(PendingPayment)
class PendingPaymentAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_filter = ['user']
    list_display = ['date', 'method', 'user', 'creator', 'amount']
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


@admin.action(description='DSGVO-Wipe Members')
def wipe_members(modeladmin, request, queryset):
    if request.POST.get('post'):
        for user in queryset.all():
            gdpr_wipe(user)
        messages.success(request, f"Es wurden {len(queryset)} Member ge-DSGVOwipe-d.")
        return None
    else:
        return render(request, "admin/wipe_members.html", context={
            "queryset": queryset,
        })

def gdpr_wipe(user):
    user.password = ''
    user.contactinfo.image.delete(False)
    user.email = ''
    user.first_name = ''
    user.last_name = ''
    user.save()

    user.contactinfo.on_intern_list = False
    user.contactinfo.intern_list_email = ''
    user.contactinfo.street = ''
    user.contactinfo.postcode = ''
    user.contactinfo.city = ''
    user.contactinfo.country = ''
    user.contactinfo.country = ''
    user.contactinfo.phone_number = ''
    user.contactinfo.birthday = None
    user.contactinfo.has_active_key = False
    user.contactinfo.key_id = ''
    user.contactinfo.remark = ''
    user.contactinfo.wiki_name = ''
    user.contactinfo.gdpr_wiped_on = date.today()
    user.contactinfo.save()

    if hasattr(user, 'paymentinfo'):
        user.paymentinfo.bank_collection_allowed = False
        user.paymentinfo.bank_account_iban = ''
        user.paymentinfo.bank_account_bic = ''
        user.paymentinfo.bank_name = ''
        user.paymentinfo.bank_account_data_of_signing = None
        user.paymentinfo.save()

    for cr in CommunicationRecord.objects.all().filter(user=user):
        cr.delete()

    user.save()


class BankCollectionModeListFilter(admin.SimpleListFilter):
    title = "bank collection mode"
    parameter_name = "bank collection mode"

    def lookups(self, request, model_admin):
        return [*BankCollectionMode.objects.all().values_list("pk", "name"), ("not_monthly", "nicht monatlich")]

    def queryset(self, request, qs):
        if self.value():
            if self.value() == "not_monthly":
                qs = qs.exclude(paymentinfo__bank_collection_mode__num_month=1)
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


class ThingUserInline(admin.TabularInline):
    model = ThingUser


class MemberCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].required = False
        self.fields["password2"].required = False

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if (password1 or password2) and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def save(self, commit=True):
        if self.cleaned_data["password1"] == '':
            self.cleaned_data["password1"] = token_urlsafe(32)
        return super().save(commit)

    class Meta(UserCreationForm.Meta):
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )


class MemberResource(resources.ModelResource):

    class Meta:
        model = User
        fields = (
            # User fields
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "is_superuser",
            "last_login",
            "date_joined",
            "groups",
            "user_permissions",
            # ContactInfo fields
            "contactinfo__on_intern_list",
            "contactinfo__intern_list_email",
            "contactinfo__in_intern_matrix_room",
            "contactinfo__matrix_handle",
            "contactinfo__street",
            "contactinfo__postcode",
            "contactinfo__city",
            "contactinfo__country",
            "contactinfo__phone_number",
            "contactinfo__birthday",
            "contactinfo__wiki_name",
            "contactinfo__image",
            "contactinfo__last_email_ok",
            "contactinfo__remark",
            "contactinfo__key_id",
            # PaymentInfo fields
            "paymentinfo__bank_collection_allowed",
            "paymentinfo__bank_collection_mode",
            "paymentinfo__bank_account_owner",
            "paymentinfo__bank_account_iban",
            "paymentinfo__bank_account_bic",
            "paymentinfo__bank_name",
            "paymentinfo__bank_account_mandate_reference",
            "paymentinfo__bank_account_date_of_signing",
        )


@admin.register(User)
class MemberAdmin(ImportExportMixin, UserAdmin):
    inlines = [
        ContactInfoInline,
        LockerInline,
        ThingUserInline,
        PaymentInfoInline,
        MembershipPeriodInline,
        CommunicationRecordInline,
        PaymentInline,
    ]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_superuser', 'is_staff'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',
                    'is_active')
    list_filter = (
        'is_staff',
        'is_superuser',
        'contactinfo__has_active_key',
        'thingusers__thing',
        BankCollectionModeListFilter,
        'paymentinfo__bank_collection_allowed',
        MembershipPeriodListFilter,
        )
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "contactinfo__intern_list_email",
        "contactinfo__matrix_handle",
        "contactinfo__street",
        "contactinfo__postcode",
        "contactinfo__city",
        "contactinfo__country",
        "contactinfo__phone_number",
        "contactinfo__birthday",
        "contactinfo__wiki_name",
        "contactinfo__remark",
        "contactinfo__key_id",
        "paymentinfo__bank_account_owner",
        "paymentinfo__bank_account_iban",
        "paymentinfo__bank_account_mandate_reference",
    )
    ordering = ('username',)
    actions = [send_welcome_mail, make_sepa_xml_for_members, export_as_csv, export_member_csv_with_fees, wipe_members]
    # allow to select/deselect for more members during actions
    list_max_show_all = 9999999
    resource_classes = [MemberResource]

    add_form = MemberCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )

    def view_on_site(self, obj):
        return f"/member/{obj.username}"


class LockerResource(resources.ModelResource):

    class Meta:
        model = Locker
        fields = (
            "name",
            "rented_by__username",
            "price",
            "comment",
        )


@admin.register(Locker)
class LockerAdmin(ImportExportModelAdmin):
    list_filter = ['rented_by']
    list_display = ['name', 'rented_by', 'price']
    resource_classes = [LockerResource]



@admin.register(BankImportMatcher)
class BankImportMatcherAdmin(admin.ModelAdmin):
    list_filter = ['action']
    list_display = ['matcher', 'comment', 'action']


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_filter = [
        'content_type',
        'user',
    ]
    search_fields = [
        'object_repr',
    ]
    list_display = [
        'action_time',
        'user',
        '__str__',
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
