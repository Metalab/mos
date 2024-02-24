from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from django.db.models import Sum

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q, F, Value
import smtplib
from django.core.mail import send_mail
# for iButton regex
from django.core.validators import RegexValidator

from easy_thumbnails.fields import ThumbnailerImageField

import string
from django.core.exceptions import ValidationError


country_codes = {
    "AD": 24,
    "AE": 23,
    "AL": 28,
    "AT": 20,
    "AX": 18,
    "AZ": 28,
    "BA": 20,
    "BE": 16,
    "BG": 22,
    "BH": 22,
    "BI": 27,
    "BL": 27,
    "BR": 29,
    "BY": 28,
    "CH": 21,
    "CR": 22,
    "CY": 28,
    "CZ": 24,
    "DE": 22,
    "DK": 18,
    "DO": 28,
    "EE": 20,
    "EG": 29,
    "ES": 24,
    "FI": 18,
    "FO": 18,
    "FR": 27,
    "GB": 22,
    "GE": 22,
    "GF": 27,
    "GG": 22,
    "GI": 23,
    "GL": 18,
    "GP": 27,
    "GR": 27,
    "GT": 28,
    "HR": 21,
    "HU": 28,
    "IE": 22,
    "IL": 23,
    "IM": 22,
    "IQ": 23,
    "IS": 26,
    "IT": 27,
    "JE": 22,
    "JO": 30,
    "KW": 30,
    "KZ": 20,
    "LB": 28,
    "LC": 32,
    "LI": 21,
    "LT": 20,
    "LU": 20,
    "LV": 21,
    "LY": 25,
    "MC": 27,
    "MD": 24,
    "ME": 22,
    "MF": 27,
    "MK": 19,
    "MQ": 27,
    "MR": 27,
    "MT": 31,
    "MU": 30,
    "NC": 27,
    "NL": 18,
    "NO": 15,
    "PF": 27,
    "PK": 24,
    "PL": 28,
    "PM": 27,
    "PS": 29,
    "PT": 25,
    "QA": 29,
    "RE": 27,
    "RO": 24,
    "RS": 22,
    "SA": 24,
    "SC": 31,
    "SD": 18,
    "SE": 24,
    "SI": 19,
    "SK": 24,
    "SM": 27,
    "ST": 25,
    "SV": 28,
    "TF": 27,
    "TL": 23,
    "TN": 24,
    "TR": 26,
    "UA": 29,
    "VA": 22,
    "VG": 24,
    "WF": 27,
    "XK": 20,
    "YT": 27,
    "YY": 34,
    "ZZ": 35,
}

def iban_letters2numbers(iban):
    """Converts all letters to the number equivalent for the IBAN validation algorithm"""
    result = []
    for char in iban:
        if char.isalpha():
            final_char = str(string.ascii_uppercase.find(char.upper()) + 10)
        else:
            final_char = char
        result.append(final_char)
    return "".join(result)

def iban_validate(iban: str) -> None:
    """Validates a given IBAN"""
    iban = iban.replace(" ","")
    if not iban.isalnum():
        raise ValidationError("IBAN can only contain numbers (0-9) and letters (A-Z)!")
    if len(iban) < 4:
        raise ValidationError("IBAN must at least 4 characters long!")
    country_code = iban[:2].upper()
    country_length = country_codes.get(country_code, False)
    if not country_length:
        raise ValidationError(f"IBAN must begin with a valid country code! ({country_code!r} is not known)")
    if not len(iban) == country_length:
        raise ValidationError(f"IBAN is not of correct length for country code {country_code!r}!")
    rearranged_iban = iban[4:] + iban[:4]
    numerized_iban = iban_letters2numbers(rearranged_iban)
    checksum = int(numerized_iban) % 97
    if checksum != 1:
        raise ValidationError("IBAN is not valid!")

class PaymentInfo(models.Model):
    bank_collection_allowed = models.BooleanField(default=False)
    bank_collection_mode = models.ForeignKey(
        'BankCollectionMode',
        on_delete=models.CASCADE,
    )
    bank_account_owner = models.CharField(max_length=200, blank=True)
    bank_account_number = models.CharField(max_length=20, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    bank_code = models.CharField(max_length=20, blank=True)
    bank_account_iban = models.CharField(max_length=34, blank=True, validators=[iban_validate])
    bank_account_bic = models.CharField(max_length=11, blank=True)
    bank_account_mandate_reference = models.CharField(max_length=35, blank=True)
    bank_account_date_of_signing = models.DateField(null=True, blank=True)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        if not self.bank_account_mandate_reference:
            self.bank_account_mandate_reference = self.user.id
        super().save(*args, **kwargs)


def get_image_path(self, filename):
    name, ext = filename.rsplit('.', 1)
    return 'userpics/%s.%s' % (self.user.username, ext)


class ContactInfo(models.Model):
    LAZZZOR_RATE_CHOICES = (
        (Decimal('1.00'), "Standard Rate (1.00)"),
        (Decimal('0.50'), "Backer's Rate (0.50)"),
    )

    on_intern_list = models.BooleanField(default=True)
    intern_list_email = models.EmailField(blank=True)

    street = models.CharField(max_length=200)
    postcode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    phone_number = models.CharField(max_length=32, blank=True)
    birthday = models.DateField(null=True, blank=True)

    wiki_name = models.CharField(max_length=50, blank=True, null=True)
    image = ThumbnailerImageField(upload_to=get_image_path, blank=True)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    last_email_ok = models.BooleanField(null=True)
    has_active_key = models.BooleanField(default=False)

    iButtonValidator = RegexValidator(r"\b[0-9]{2}-[0-9a-zA-Z]{12}\b", "iButton ID entspricht nicht dem Format [0-9]{2}-[0-9a-zA-Z]{12}")
    key_id = models.CharField(max_length=15, blank=True, null=True, validators=[iButtonValidator])

    remark = models.TextField(null=True, blank=True)

    def get_membership_fees(self):
        mp_list = MembershipPeriod.objects.filter(user=self.user)
        fees = list(MembershipFee.objects.all())

        for mp in mp_list:
            for month in mp.get_months():
                fee = mp.get_membership_fee(month, fees)
                if fee.amount > 0:
                    yield (month, fee.amount)

    def get_debts(self):
        arrears = sum(f[1] for f in self.get_membership_fees())
        return arrears - self.get_all_payments()

    def get_debts_detailed(self):
        fees = ({"date": f[0], "amount": -f[1], "kind": "membership fee"} for f in self.get_membership_fees())
        payments = ({"date": p.date, "amount": p.amount, "kind": p.method.name} for p in Payment.objects.filter(user=self.user))
        movements = [*fees, *payments]
        movements.sort(key=lambda m: m["date"])

        balance = 0

        for movment in movements:
            balance += movment["amount"]
            movment["balance"] = balance

        movements.reverse()
        return movements

    def get_debt_for_month(self, date_in_month):
        # see if the there is a membership period for the month
        mp_list = MembershipPeriod.objects.filter(Q(begin__lte=date_in_month),
                                                  Q(end__isnull=True) | Q(end__gte=date_in_month),
                                                  user=self.user)

        if not mp_list.exists():
            return 0
        else:
            # find the membership fee for the month and kind
            # of membership and return amount
            mp = mp_list[0]
            fee = mp.kind_of_membership.membershipfee_set.filter(
                Q(start__lte=date_in_month),
                Q(end__isnull=True) | Q(end__gte=date_in_month))[0]

            return fee.amount

    def get_debt_for_this_month(self):
        return self.get_debt_for_month(date.today())

    def get_all_payments(self):
        return Payment.objects.filter(user=self.user).aggregate(Sum('amount'))['amount__sum'] or 0

    def get_date_of_first_join(self):
        mp = MembershipPeriod.objects.filter(user=self.user).order_by('begin').first()
        return mp.begin if mp else None

    def get_wikilink(self):
        wikiname = self.wiki_name or self.user.username

        return u'%sBenutzer:%s' % (settings.HOS_WIKI_URL, wikiname)

    def send_mail(self, subject, body, log_file=None):
        try:
            send_mail(
                subject,
                body,
                settings.HOS_ANNOUNCE_FROM,
                [self.user.email],
                fail_silently=False,
            )
            self.last_email_ok = True
            self.save()
        except smtplib.SMTPException as e:
            if log_file:
                with open(log_file, 'a') as f:
                    f.write('\n\n'+self.user.email)
                    f.write('\n'+repr(e))
            self.last_email_ok = False
            self.save()

def get_mailinglist_members():
    return User.objects.filter(
                Q(membershipperiod__end__isnull=True) |
                Q(membershipperiod__end__gte=datetime.now()))\
                .distinct()


def get_active_members_for(dt):
    return User.objects.filter(
                Q(membershipperiod__begin__lte=dt),
                Q(membershipperiod__end__isnull=True) |
                Q(membershipperiod__end__gte=dt))\
                .distinct()


def get_active_members():
    return get_active_members_for(datetime.now())


def get_active_and_future_members():
    return User.objects.filter(
                Q(membershipperiod__end__isnull=True) |
                Q(membershipperiod__end__gte=datetime.now()))\
                .distinct()


def members_due_for_bank_collection(users=None):
    if users is None:
        users = get_active_members()

    current_month = datetime.now().month

    users = users.filter(paymentinfo__bank_collection_allowed=True)
    users = users.filter(paymentinfo__bank_collection_mode__num_month__gt=0)
    users = users.annotate(
        is_collectable=Value(current_month - 1) % F("paymentinfo__bank_collection_mode__num_month"),
    )
    users = users.filter(is_collectable=0)

    return users


def get_active_membership_months_until(date):
    periods = MembershipPeriod.objects.filter(Q(begin__lte=date))
    res = {}
    for p in periods:
        begin = get_months(p.begin)
        end = get_months(date if p.end is None or p.end > date else p.end)
        nrMonths = end - begin + 1
        kind = p.kind_of_membership.name
        if kind in res:
            res[kind] += nrMonths
        else:
            res[kind] = nrMonths

    return res


def get_months(date):
    return date.month + 12 * date.year


class BankCollectionMode(models.Model):
    name = models.CharField(max_length=20)
    num_month = models.IntegerField()

    def __str__(self):
        return self.name


def get_month_list(cur, end):
    if end is None or end >= date.today():
        end = date.today()

    while cur < end:
        yield cur
        cur = cur + relativedelta(months=1)


class MembershipPeriod(models.Model):
    begin = models.DateField()
    end = models.DateField(null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    kind_of_membership = models.ForeignKey(
        'KindOfMembership',
        on_delete=models.CASCADE,
    )
    comment = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_duration_in_month(self):
        if self.end is None or self.end > date.today():
            end = date.today()
        else:
            end = self.end
        if end < self.begin:
            return 0

        begin = date(self.begin.year, self.begin.month, 1)
        end = date(end.year, end.month, 2)

        month = 0
        while begin < end:
            if begin.month == 12:
                begin = date(begin.year + 1, 1, 1)
            else:
                begin = date(begin.year, begin.month + 1, 1)
            month += 1
        return month

    def get_membership_fee(self, month, fees=None):
        if fees is None:
            fees = list(MembershipFee.objects.all())
        for fee in fees:
            if fee.kind_of_membership_id == self.kind_of_membership_id and fee.start <= month and (fee.end is None or fee.end >= month):
                return fee
        raise Exception(f"could not find a membership fee for month {month} and kind of membership {self.kind_of_membership}")

    def get_months(self):
        return get_month_list(self.begin, self.end)


class MembershipFee(models.Model):
    """
    Defines the membership fee for a certain period of time.
    With this class it is possible to define different amount of
    membership fees for different periods of time and for different
    kind of members, e.g. pupils, unemployees, normal members, ...
    """

    kind_of_membership = models.ForeignKey(
        'KindOfMembership',
        on_delete=models.CASCADE,
    )
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    amount = models.IntegerField()

    def __str__(self):
        return "%s - %d" % (self.kind_of_membership, self.amount)


class KindOfMembership(models.Model):
    FULL_SPIND_CHOICES = (
        ('no', "0 Spind", 0),
        ('small_1', "1 kleiner Spind", 8),
        ('big_1', "1 großer Spind", 10),
        ('small_2', "2 kleiner Spind", 16),
    )
    SPIND_FEES = {c[0]: c[2] for c in FULL_SPIND_CHOICES}
    SPIND_CHOICES = ((c[0], f"{c[1]} ({c[2]}€)") for c in FULL_SPIND_CHOICES)
    FEE_CATEGORY = (
        ('standard', 'standard'),
        ('free', 'free'),
        ('decreased', 'ermäßigt'),
        ('increased', 'erhöht'),
    )

    name = models.CharField(max_length=30)
    spind = models.CharField(choices=SPIND_CHOICES, max_length=7, default="no")
    fee_category = models.CharField(choices=FEE_CATEGORY, max_length=9, default="standard")

    @property
    def spind_fee(self):
        return self.SPIND_FEES[self.spind]

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AbstractPayment(models.Model):
    amount = models.FloatField()
    comment = models.CharField(max_length=200, blank=True)
    date = models.DateField()
    method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )
    original_file = models.CharField(max_length=200, null=True)

    def __str__(self):
        return u"%s, %s, %s, %s" % (self.date, self.amount, self.user.username, self.method.name)

    class Meta:
        ordering = ['date']
        abstract = True


# created by SEPA XML export and converted to an actual payment manually in admin
class PendingPayment(AbstractPayment):
    pass


class Payment(AbstractPayment):
    original_line = models.TextField(blank=True)
    original_lineno = models.IntegerField(blank=True, null=True)


class MailinglistMail(models.Model):
    email = models.EmailField()
    on_intern_list = models.BooleanField(default=True)

    def __str__(self):
        return self.email

class Locker(models.Model):
    name = models.CharField(max_length=80)
    comment = models.TextField(blank=True)
    price = models.IntegerField()
    rented_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

class BankImportMatcher(models.Model):
    MATCHER_CHOICES = (
        ('drop', "drop"),
        ('do_not_match', "do not match"),
        ('match_to', "match to"),
        ('color', "color"),
    )

    matcher = models.CharField(max_length=80, help_text="match in IBAN, sender, text")
    comment = models.CharField(max_length=200, null=True, blank=True)
    action = models.CharField(choices=MATCHER_CHOICES, max_length=20)
    color = models.CharField(max_length=100, null=True, blank=True, help_text="if action=color, e.g. 'red' or 'rgba(255,0,0,0.1)'")
    member = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, help_text="if action=match_to")
