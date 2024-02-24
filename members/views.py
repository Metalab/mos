from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import DefaultDict
from dateutil import relativedelta
from sepaxml import SepaDD
import json

from dateutil.rrule import rrule, MONTHLY
from django.contrib import messages
from django.db.models import Q
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

from .forms import UserEmailForm, UserNameForm, UserAdressForm,\
    UserImageForm, UserInternListForm
from .models import ContactInfo, get_active_members, \
    get_active_and_future_members, Payment, PendingPayment, PaymentMethod, \
    get_mailinglist_members, get_month_list, KindOfMembership, \
    MembershipPeriod, MembershipFee, BankImportMatcher
from .util import get_list_of_history_entries


def members_history(request):
    history_entry_list = get_list_of_history_entries()
    months = list(rrule(MONTHLY, dtstart=date(2006, 3, 1), until=date.today()))

    history_list = [history_entry_list[dt.date()] for dt in months]

    history_list.reverse()
    context = {'list': history_list}
    return render(request, 'members/members_history.html', context)


@login_required
def hetti(request):
    if not request.user.is_superuser:
        return HttpResponseNotAllowed('you are not allowed to use the hetti')

    def parse_date(s):
        return date(*(int(c) for c in s.split('-')))

    try:
        end_date = parse_date(request.GET["end_date"])
    except KeyError:
        end_date = date(date.today().year, date.today().month, 1)
    except Exception as ex:
        return HttpResponseBadRequest(str(ex), content_type="text/plain")

    try:
        start_date = parse_date(request.GET["start_date"])
    except KeyError:
        start_date = end_date - relativedelta.relativedelta(years=2)
    except Exception as ex:
        return HttpResponseBadRequest(str(ex), content_type="text/plain")

    months = []

    # all of the following is very slow, but we're only dealing with 24 months
    fees = list(MembershipFee.objects.all())

    for month in get_month_list(start_date, end_date):
        first_day_of_month = month
        first_day_of_next_month = month + relativedelta.relativedelta(months=1)

        month_statistics = {
            "month": month,
            "spind_kinds": defaultdict(int),
            "fee_category_kinds": defaultdict(int),
        }

        periods = MembershipPeriod.objects.filter(Q(begin__lte=month), Q(end__isnull=True) | Q(end__gte=month))

        for kind in KindOfMembership.objects.all():
            count = periods.filter(kind_of_membership=kind).count()
            if count > 0:
                month_statistics["spind_kinds"][kind.get_spind_display()] += count
                month_statistics["fee_category_kinds"][kind.get_fee_category_display()] += count

        month_statistics["total_fees"] = 0
        month_statistics["total_fees_spind"] = 0
        month_statistics["total_fees_membership"] = 0

        for period in periods:
            fee_spind = period.kind_of_membership.spind_fee
            fee_membership = period.get_membership_fee(month, fees).amount - fee_spind

            month_statistics["total_fees"] += fee_spind + fee_membership
            month_statistics["total_fees_spind"] += fee_spind
            month_statistics["total_fees_membership"] += fee_membership

        month_statistics["total_payments"] = Payment.objects.filter(
            date__gte=first_day_of_month,
            date__lt=first_day_of_next_month,
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        month_statistics["spind_kinds"] = dict(month_statistics["spind_kinds"])
        month_statistics["fee_category_kinds"] = dict(month_statistics["fee_category_kinds"])
        months.append(month_statistics)

    context = {'months': months}
    return render(request, 'members/members_hetti.html', context)


@csrf_exempt
def valid_user(request):
    # #tyrsystem
    # I'm no sure what this comment means... "Tuer-System"? I've found entries
    # in Apache's log file no younger than a year. Probably this is not used
    # anymore.
    if not request.is_secure():
        raise Http404()
    user_cache = authenticate(
        username=request.POST.get('user'),
        password=request.POST.get('pass')
    )
    if user_cache and user_cache.is_active:
        return HttpResponse('OK')
    return HttpResponse('FAIL', status=403)


def members_details(request, user_username, errors="", update_type=""):
    context = {'item': get_object_or_404(User, username=user_username),
               'ea': request.user.username == user_username,
               'error_form': errors, 'error_type': update_type}

    return render(request, 'members/members_details.html', context)


def members_update(request, user_username, update_type):
    if request.method != "POST" or not request.user.username == user_username:
        return members_details(request, user_username,
                               "no permission to edit settings", "permission")
    user = get_object_or_404(User, username=user_username)

    error_form = False
    error_type = False

    if update_type == "email" and request.method == "POST":
        update_form = UserEmailForm(request.POST, instance=user)

    elif update_type == "name" and request.method == "POST":
        update_form = UserNameForm(request.POST, instance=user)

    elif update_type == "adress" and request.method == "POST":
        contact_info = get_object_or_404(ContactInfo, user=user)
        update_form = UserAdressForm(request.POST, instance=contact_info)

    elif update_type == "internlist" and request.method == "POST":
        contact_info = get_object_or_404(ContactInfo, user=user)
        update_form = UserInternListForm(request.POST, instance=contact_info)

    if update_form.is_valid():
        update_form.save()
    else:
        error_form = update_form
        error_type = update_type

    return members_details(request, user_username, error_form, error_type)


@login_required
def members_bank(request):
    if not request.user.is_superuser:
        return HttpResponseNotAllowed('you are not allowed to use this method')
    return render(request, 'members/member_bank.html')

class SepaException(Exception):
    pass

def generate_sepa(admin_user, members_to_collect_from):
    if len(members_to_collect_from) == 0:
        raise SepaException("no members to collect from.")

    sepa = SepaDD({
        "name": settings.HOS_SEPA_CREDITOR_NAME,
        "IBAN": settings.HOS_SEPA_CREDITOR_IBAN,
        "BIC": settings.HOS_SEPA_CREDITOR_BIC,
        "batch": settings.HOS_SEPA_BATCH,
        "creditor_id": settings.HOS_SEPA_CREDITOR_ID,
        "currency": settings.HOS_SEPA_CURRENCY,
        "instrument": 'CORE'
    }, schema=settings.HOS_SEPA_SCHEMA)

    sepaxml_filename = f'metalab_sepa_{date.today().year}_{format(date.today().month, "02")}.xml'
    payment_comment = f'{sepaxml_filename} exported {datetime.now().replace(microsecond=0).isoformat()} by {admin_user.username}'
    payment_method = PaymentMethod.objects.get(name='bank collection')

    if not payment_method:
        raise SepaException("could not find PaymentMethod 'bank collection'")

    for member in members_to_collect_from:
        debt = member.contactinfo.get_debt_for_month(date.today())

        if debt > 0:
            pmi = member.paymentinfo
            # on the first debit initiation, set the mandate signing date
            if not pmi.bank_account_date_of_signing:
                pmi.bank_account_date_of_signing = date.today()
                pmi.save()
                payment_type = "FRST"
                collection_date = date.today() + timedelta(days=+5)
            else:
                payment_type = "RCUR"
                collection_date = date.today() + timedelta(days=+3)

            sepa.add_payment({
                "name": pmi.bank_account_owner,
                "IBAN": pmi.bank_account_iban.replace(' ', ''),
                "mandate_id": pmi.bank_account_mandate_reference,
                "mandate_date": pmi.bank_account_date_of_signing,
                "type": payment_type,
                "collection_date": collection_date,
                "amount": debt * 100,  # in cents
                "execution_date": date.today(),
                "description": f'Mitgliedsbeitrag {date.today().year}/{date.today().month} (u{member.id})',
            })

            PendingPayment.objects.create(
                date = collection_date,
                user = member,
                amount = debt,
                method = payment_method,
                original_file = sepa.msg_id,
                comment = payment_comment,
            )

    return sepa, sepaxml_filename

@login_required
def members_bank_json_import(request):
    if not request.user.is_superuser:
        return HttpResponseNotAllowed('you are not allowed to use this method')
    if request.method != "POST" or not 'erstejson' in request.FILES:
        messages.error(request, 'No file found.')
        return redirect("/member/bank/")

    try:
        payments = json.load(request.FILES['erstejson'])
    except json.JSONDecodeError:
        messages.error(request, 'could not parse JSON data')
        return redirect("/member/bank/")

    matchers = list(BankImportMatcher.objects.all())

    import_rows = []

    for payment in payments:
        if not payment["partnerName"]:
            continue
        if payment["amount"]["currency"] != "EUR":
            continue

        try:
            iban = payment["partnerAccount"]["iban"]
        except LookupError:
            continue

        payment["amount"]["value_full"] = payment["amount"]["value"] / pow(10, payment["amount"]["precision"])
        payment["booking"] = datetime.fromisoformat(payment["booking"])
        payment["text"] = (payment["reference"] + " " + payment["receiverReference"]).strip()

        should_drop = False
        should_match = (payment["amount"]["value_full"] > 0 or "Rückleitung" in payment["reference"])
        color = ""
        matched_members = []

        for matcher in matchers:
            fields = [
                payment["partnerName"],
                payment["partnerAccount"]["iban"],
                payment["text"],
            ]

            if any(matcher.matcher in f for f in fields):
                if matcher.action == "color" and matcher.color:
                    color = matcher.color
                elif matcher.action == "do_not_match":
                    should_match = False
                elif matcher.action == "match_to" and matcher.member:
                    matched_members = [matcher.member]
                    should_match = False
                elif matcher.action == "drop":
                    should_drop = True

        if should_drop:
            continue

        if Payment.objects.filter(original_line=payment["referenceNumber"]).exists():
            color = "rgba(0, 0, 0, 0.2)"
            should_match = False

        if should_match:
            matched_members = User.objects.filter(paymentinfo__bank_account_iban=iban)

        import_rows.append({
            "payment": payment,
            "matched_members": matched_members,
            "color": color,
        })

    all_members = User.objects.filter(Q(membershipperiod__isnull=False)).distinct()

    return render(request, 'members/member_bank_json_match.html', context={
        "import_rows": import_rows,
        "all_members": all_members,
        "upload_filename": request.FILES['erstejson'].name,
    })


@login_required
def members_bank_json_match(request):
    if not request.user.is_superuser:
        return HttpResponseNotAllowed('you are not allowed to use this method')
    if request.method != "POST" or not request.POST:
        messages.error(request, 'No data found.')
        return redirect("/member/bank/")

    fields = [
        "text",
        "referenceNumber",
        "member_pk",
        "value",
        "date",
    ]

    lines = [
        {f: request.POST.getlist(f + "[]")[r] for f in fields}
        for r in range(len(request.POST.getlist(fields[0] + "[]")))
    ]

    bank_collection = PaymentMethod.objects.get(name="bank collection")
    bank_transfer = PaymentMethod.objects.get(name="bank transfer")

    count = 0

    for line in lines:
        if not line["member_pk"]:
            continue

        # all of MOS money is in float. don't ask.
        line["value"] = float(line["value"])

        Payment.objects.create(
            date=datetime.strptime(line["date"], "%Y-%m-%d"),
            user_id=line["member_pk"],
            amount=line["value"],
            comment=line["text"][:200],
            # Rückleitungen als BankCollection, alle anderen BankTransfer
            method=bank_collection if line["value"] < 0 else bank_transfer,
            original_file=request.POST["upload_filename"],
            original_line=line["referenceNumber"],
        )
        count += 1

    messages.success(request, f"imported {count} payments from {request.POST['upload_filename']}")

    return redirect("/member/bank")


def members_key_list(request):
    # get active members with active keys
    members_with_keys = get_active_and_future_members().filter(contactinfo__has_active_key=True).filter(contactinfo__key_id__isnull=False)

    # just output keys one line per key
    text = '\r\n'.join([x.contactinfo.key_id for x in members_with_keys])
    return HttpResponse(text, content_type='text/plain')


def members_intern_list(request):
    members_on_intern = get_mailinglist_members() \
        .filter(contactinfo__on_intern_list = True) \
        .exclude(contactinfo__intern_list_email = '')
    addresses = [m.contactinfo.intern_list_email for m in members_on_intern]
    return HttpResponse('\r\n'.join(addresses), content_type='text/plain')

def members_update_userpic(request, user_username):
    if not request.user.username == user_username:
        return members_details(request, user_username,
                               "no permission to edit settings", "permission")

    if request.method == "POST":
        user = get_object_or_404(User, username=user_username)
        contact_info = get_object_or_404(ContactInfo, user=user)
        image_form = UserImageForm(request.POST, request.FILES,
                                   instance=contact_info)
        if image_form.is_valid():
            image_data = image_form.save()
            image_data.save()
            # return to userpage if upload was successful
            return members_details(request, user_username)
    else:
        image_form = UserImageForm()

    context = {'form': image_form}
    return render(request, 'members/member_update_userpic.html', context)
