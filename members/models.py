#encoding=utf-8
from __future__ import unicode_literals, print_function

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from decimal import Decimal

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible, smart_unicode, force_str


class PaymentInfo(models.Model):
    bank_collection_allowed = models.BooleanField(default=False)
    bank_collection_mode = models.ForeignKey('BankCollectionMode')
    bank_account_owner = models.CharField(max_length=200, blank=True)
    bank_account_number = models.CharField(max_length=20, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    bank_code = models.CharField(max_length=20, blank=True)
    bank_account_iban = models.CharField(max_length=34, blank=True)
    bank_account_bic = models.CharField(max_length=11, blank=True)
    bank_account_mandate_reference = models.CharField(max_length=35, blank=True)
    bank_account_date_of_signing = models.DateField(null=True, blank=True)

    user = models.OneToOneField(User)


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
    image = models.ImageField(upload_to=get_image_path, blank=True)

    user = models.OneToOneField(User)

    last_email_ok = models.NullBooleanField()
    has_active_key = models.BooleanField(default=False)
    has_lazzzor_privileges = models.BooleanField(default=False)
    key_id = models.CharField(max_length=100, blank=True, null=True)

    lazzzor_rate = models.DecimalField(choices=LAZZZOR_RATE_CHOICES, default='1.00',
                                       max_digits=3, decimal_places=2)
    remark = models.TextField(null=True, blank=True)

    def get_debts(self):
        # FIXME: this is broken because it assumes that a membership period
        #       has a constant fee
        arrears = 0
        mp_list = MembershipPeriod.objects.filter(user=self.user)
        for mp in mp_list:
            for month in mp.get_months():
                fee = MembershipFee.objects.get(
                    Q(kind_of_membership=mp.kind_of_membership),
                    Q(start__lte=month),
                    Q(end__isnull=True) | Q(end__gte=month)
                )
                if fee.amount > 0:
                    arrears += fee.amount
        return arrears - self.get_all_payments()

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

    def get_all_payments(self):
        payments = 0
        p_list = Payment.objects.filter(user=self.user)
        for p in p_list:
            payments += p.amount
        return payments

    def get_date_of_entry(self):
        # FIXME: the order here is wrong, didn't change it since i don't have time to check all implications
        #                    sf - 2010 07 27
        mp = MembershipPeriod.objects.filter(user=self.user).order_by('-begin').first()
        return mp.begin if mp else None

    def get_current_membership_period(self):
        # FIXME: the order here is wrong, didn't change it since i don't have time to check all implications
        #                    sf - 2010 07 27
        mp = MembershipPeriod.objects.filter(user=self.user)\
            .order_by('begin')[0]
        if mp.end is None:
            return mp
        else:
            return None
        return mp.begin

    def is_active_key_member(self):
        # FIXME: the order here is wrong, didn't change it since i don't have time to check all implications
        #                    sf - 2010 07 27
        mp = MembershipPeriod.objects.filter(user=self.user)\
            .order_by('-begin')[0]
        if mp.end is not None:
            return False

        return self.key_id is not None and self.has_active_key

    def get_wikilink(self):
        wikiname = self.wiki_name or self.user.username

        return u'%sBenutzer:%s' % (settings.HOS_WIKI_URL, wikiname)


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


@python_2_unicode_compatible
class BankCollectionMode(models.Model):
    name = models.CharField(max_length=20)
    num_month = models.IntegerField()

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class MembershipPeriod(models.Model):
    begin = models.DateField()
    end = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User)
    kind_of_membership = models.ForeignKey('KindOfMembership')

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

    def get_months(self):
        cur = self.begin
        end = self.end
        if end is None or end >= date.today():
            end = date.today()

        while cur < end:
            yield cur
            cur = cur + relativedelta(months=1)


@python_2_unicode_compatible
class MembershipFee(models.Model):
    """
    Defines the membership fee for a certain period of time.
    With this class it is possible to define different amount of
    membership fees for different periods of time and for different
    kind of members, e.g. pupils, unemployees, normal members, ...
    """

    kind_of_membership = models.ForeignKey('KindOfMembership')
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    amount = models.IntegerField()

    def __str__(self):
        return "%s - %d" % (self.kind_of_membership, self.amount)


@python_2_unicode_compatible
class KindOfMembership(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class PaymentManager(models.Manager):
    def import_smallfile(self, filename, date):
        import csv

        f = open(filename, 'r')
        r = csv.reader(f, delimiter=force_str(';'))

        for line in r:
            if len(line) < 2:
                print(line)
                continue
            try:
                u = User.objects.get(first_name=smart_unicode(line[0]), last_name=smart_unicode(line[1]))
            except User.DoesNotExist:
                print(line)
                continue
            except:
                print("exception on line:")
                print(line)
                raise

            sum = line[5]
            try:
                Payment.objects.create(date=date, user=u, amount=sum, method=PaymentMethod.objects.get(name='bank collection'), original_file=filename, original_line=str(line))
            except ValueError:
                print(line)

    # used to import generic payments, including date and payment type (as opposed to import_smallfile)
    def import_generic(self, filename):
        import csv

        f = open(filename, 'r')
        r = csv.reader(f, delimiter=force_str(';'))

        for line in r:
            if len(line) < 9:
                print('malformed:', repr(line))
                continue
            try:
                u = User.objects.get(first_name=smart_unicode(line[0]), last_name=smart_unicode(line[1]))
            except User.DoesNotExist:
                print('user not found:', repr(line))
                continue

            sum, date, method = (line[5], line[7], line[8])
            try:
                p = Payment.objects.filter(date=date, amount=sum, user=u)
                if len(p) != 0:
                    print('payment already present:', repr(line))
                    continue
                Payment.objects.create(date=date, user=u, amount=sum, method=PaymentMethod.objects.get(name=method), original_file=filename, original_line=str(line))
                print('created:', repr(line))
            except ValueError:
                print('error creating payment:', repr(line))

    def import_hugefile(self, filename):
        import csv

        f = open(filename, 'r')
        r = csv.reader(f, delimiter=force_str(';'))

        i = 0
        for line in r:
            i += 1
            if not line[0]:
                continue

            if line[3] in ('sammler', 'Umlaufvermögen:2810 Bank'):
                pms_name = 'bank collection'
            else:
                pms_name = line[3]
            pms = PaymentMethod.objects.filter(name=pms_name)
            if pms:
                pm = pms[0]
            else:
                pm = PaymentMethod.objects.all()[0]

            subject = line[2]

            if '(' in subject and ')' in subject:
                list_str = subject.split('(')[1].split(')')[0]
                if list_str == '280':
                    list = [subject.split('(')[0]]
                else:
                    list = list_str.split(',')
            else:
                list = [subject]

            sum = line[5] if line[5] else '-'+line[4] if line[4] else '0'

            sum = sum.replace(',', '.')

            try:
                sum = Decimal(sum) / len(list)
            except Exception, e:
                print(e)
                print(line)
                continue

            for name in list:
                fragments = name.split(' ')

#                if line[0] == '2007-10-02':
#                    print name, fragments

                if fragments[0] == '':
                    fragments = fragments[1:]

                if len(fragments) == 0:
                    print('aaaaaaaaaahhh!!')
                    continue

                if fragments[0] == 'fehlgeschlagen':
                    fragments = fragments[1:]

                if 'ckzahlung' in fragments[0]:
                    fragments = fragments[1:]

                if fragments[0] == 'Ewald-Oliver':
                    fragments[0] = 'Oliver'

                if len(fragments) > 1:
                    if fragments[1] in ('Sirek', 'Siereck'):
                        fragments[1] = 'Sierek'

                    if fragments[1] == 'Eckhardt':
                        fragments[1] = 'Eckardt'

                    if fragments[1] == 'Grenzfurtner':
                        fragments[1] = 'Grenzfurthner'

                    if fragments[1] in ('Berg',):  # Berg San, Leo Findeisen
                        fragments = fragments[1:]

                    if fragments[1] in ('Leo',):
                        fragments = [fragments[0], fragments[2]]

                    if fragments[0] == 'Schreiner':
                        fragments = [fragments[1], fragments[0]]

                    if fragments[1] == 'Manztos':
                        fragments[1] = 'Mantzos'

                    if len(fragments) > 2 and fragments[2]:
                        if fragments[2] == 'Laub':
                            fragments = fragments[1:]

                if(len(fragments) > 1):
                    u = User.objects.filter(first_name__iexact=fragments[0], last_name__iexact=fragments[1])
                    if len(u) != 1:
                        print(u, fragments)
                    else:
                        Payment.objects.create(user=u[0], amount=sum,
                                               date=line[0], method=pm,
                                               original_line=str(line),
                                               original_file=filename,
                                               original_lineno=i)

                else:
                    print('no user found for')
                    print(line)


@python_2_unicode_compatible
class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Payment(models.Model):
    amount = models.FloatField()
    comment = models.CharField(max_length=200, blank=True)
    date = models.DateField()
    method = models.ForeignKey(PaymentMethod)
    user = models.ForeignKey(User, null=True)
    original_line = models.TextField(blank=True)
    original_file = models.CharField(max_length=200, null=True)
    original_lineno = models.IntegerField(blank=True, null=True)

    objects = PaymentManager()

    def __str__(self):
        return u"%s, %s, %s, %s" % (self.date, self.amount, self.user.username, self.method.name)

    class Meta:
        ordering = ['date']
