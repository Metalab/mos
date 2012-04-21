#!/usr/bin/python
# vim: set fileencoding=utf-8

import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import admin
from django.utils.encoding import smart_unicode



class PaymentInfo(models.Model):
    bank_collection_allowed = models.BooleanField()
    bank_collection_mode = models.ForeignKey('BankCollectionMode')
    bank_account_owner = models.CharField(max_length=200, blank=True)
    bank_account_number = models.CharField(max_length=20, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    bank_code = models.CharField(max_length=20, blank=True)

    user = models.ForeignKey(User, unique=True)


class ContactInfo(models.Model):

    def get_image_path(self, filename):
        name, ext = filename.rsplit('.', 1)
        return 'userpics/%s.%s' %(self.user.username, ext)

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

    user = models.ForeignKey(User, unique=True)

    last_email_ok = models.NullBooleanField(null=True)
    has_active_key = models.BooleanField(null=False)
    key_id = models.CharField(max_length=100, blank=True, null=True)


    remark = models.TextField(null=True, blank=True)


    def get_debts(self):
        #FIXME: this is broken because it assumes that a membership period
        #       has a constant fee
        arrears = 0
        mp_list = MembershipPeriod.objects.filter(user=self.user)
        for mp in mp_list:
            fee = MembershipFee.objects.get(kind_of_membership=\
                                                mp.kind_of_membership)
            if fee.amount > 0:
                arrears += mp.get_duration_in_month()*fee.amount
        return arrears - self.get_all_payments()

    def get_debt_for_month(self, date_in_month):
        #see if the there is a membership period for the month
        mp_list = MembershipPeriod.objects.filter(user=self.user).filter(
                    Q(begin__lte=date_in_month),
                    Q(end__isnull=True) | Q(end__gte=date_in_month))

        if mp_list.count() == 0:
            return 0
        else:
           #find the membership fee for the month and kind
            #of membership and return amount
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
        mp = MembershipPeriod.objects.filter(user=self.user)\
            .order_by('-begin')[0]
        return mp.begin

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
        if not mp.end is None:
            return False

        return not self.key_id is None and self.has_active_key

    def get_wikilink(self):
	wikiname = self.wiki_name
        if not wikiname:
            wikiname = self.user.username

	return u'%sBenutzer:%s' % (settings.HOS_WIKI_URL, wikiname)


def get_active_members():
    return User.objects.filter(
                Q(membershipperiod__begin__lte=datetime.datetime.now()),
                Q(membershipperiod__end__isnull=True) |
                Q(membershipperiod__end__gte=datetime.datetime.now()))\
                .distinct()

def get_mailinglist_members():
    return User.objects.filter(
                Q(membershipperiod__end__isnull=True) |
                Q(membershipperiod__end__gte=datetime.datetime.now()))\
                .distinct()

def get_active_members_for(dt):
    return User.objects.filter(
                Q(membershipperiod__begin__lte=dt),
                Q(membershipperiod__end__isnull=True) |
                Q(membershipperiod__end__gte=dt))\
                .distinct()

def get_active_and_future_members():
    return User.objects.filter(
                Q(membershipperiod__end__isnull=True) |
                Q(membershipperiod__end__gte=datetime.datetime.now()))\
                .distinct()

def get_active_membership_months_until(date):
    periods = MembershipPeriod.objects.filter(Q(begin__lte=date))
    res = {}
    for p in periods:
        begin = get_months(p.begin)
        end = get_months(date if p.end is None or p.end > date else p.end)
        nrMonths = end - begin + 1
        kind = p.kind_of_membership.name
        if res.has_key(kind):
            res[kind] += nrMonths
        else:
            res[kind] = nrMonths

    return res

def get_months(date):
    return date.month + 12*date.year

class BankCollectionMode(models.Model):
    name = models.CharField(max_length=20)
    num_month = models.IntegerField()

    def __unicode__(self):
        return u"%s" % self.name


class MembershipPeriod(models.Model):
    begin = models.DateField()
    end = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User)
    kind_of_membership = models.ForeignKey('KindOfMembership')

    def __unicode__(self):
        return u"%s" % self.user.username

    def get_duration_in_month(self):
        if self.end is None:
            end = datetime.date.today()
        else:
            end = self.end
        if end < self.begin:
            return 0

        begin = datetime.date(self.begin.year, self.begin.month, 1)
        end = datetime.date(end.year, end.month, 2)

        month = 0
        while begin < end:
            if begin.month == 12:
                begin = datetime.date(begin.year + 1, 1, 1)
            else:
                begin = datetime.date(begin.year, begin.month + 1, 1)
            month += 1
        return month


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

    def __unicode__(self):
        return u"%s - %d" % (self.kind_of_membership, self.amount)


class KindOfMembership(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return u"%s" % self.name


class PaymentManager(models.Manager):
    def import_smallfile(self, filename, date):
        import csv

        f = open(filename, 'r')
        r = csv.reader(f, delimiter=";")

        for line in r:
            if len(line)<2:
                print line
                continue
            try:
                u = User.objects.get(first_name=smart_unicode(line[0]), last_name=smart_unicode(line[1]))
            except User.DoesNotExist:
                print line
                continue

            sum = line[5]
            try:
                Payment.objects.create(date=date, user=u, amount=sum, method=PaymentMethod.objects.get(name='bank collection'), original_file=filename, original_line=str(line))
            except ValueError, e:
                print line


    def import_hugefile(self, filename):
        import csv
        from decimal import Decimal

	f = open(filename, 'r')
        r = csv.reader(f, delimiter=";")

        i=0

        for line in r:
            i+=1
            if not line[0]:
                continue
            pms = PaymentMethod.objects.filter(name=line[3] if not line[3] in ('sammler', 'Umlaufvermögen:2810 Bank') else 'bank collection')
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
                print e
                print line
                continue

            for name in list:
                fragments = name.split(' ')

#                if line[0] == '2007-10-02':
#                    print name, fragments

                if fragments[0] == '':
                    fragments = fragments[1:]

                if len(fragments)==0:
                    print 'aaaaaaaaaahhh!!'
                    continue

                if fragments[0] == 'fehlgeschlagen':
                    fragments = fragments[1:]

                if 'ckzahlung' in fragments[0]:
                    fragments = fragments[1:]

                if fragments[0] == 'Ewald-Oliver':
                    fragments[0] = 'Oliver'


                if len(fragments)>1:
                    if fragments[1] in ('Sirek', 'Siereck'):
                        fragments[1] = 'Sierek'

                    if fragments[1] == 'Eckhardt':
                        fragments[1] = 'Eckardt'

                    if fragments[1] == 'Grenzfurtner':
                        fragments[1] = 'Grenzfurthner'

                    if fragments[1] in ('Berg',): # Berg San, Leo Findeisen
                        fragments = fragments[1:]

                    if fragments[1] in ('Leo',):
                        fragments = [fragments[0], fragments[2]]

                    if fragments[0] == 'Schreiner':
                        fragments = [fragments[1] , fragments[0]]

                    if fragments[1] == 'Manztos':
                        fragments[1] = 'Mantzos'

                    if len(fragments)>2 and fragments[2]:
                        if fragments[2] == 'Laub':
                            fragments = fragments[1:]

                if(len(fragments)>1):
                    u = User.objects.filter(first_name__iexact=fragments[0], last_name__iexact=fragments[1])
                    if len(u)!=1:
                        print u, fragments
                    else:
                        Payment.objects.create(user=u[0], amount=sum, date=line[0], method=pm, original_line = str(line), original_file = filename, original_lineno = i)


                else:
                    print 'no user found for'
                    print line
        pass

class Payment(models.Model):
    amount = models.FloatField()
    comment = models.CharField(max_length=200, blank=True)
    date = models.DateField()
    method = models.ForeignKey('PaymentMethod')
    user = models.ForeignKey(User, null=True)
    original_line = models.TextField(blank=True)
    original_file = models.CharField(max_length=200, null=True)
    original_lineno = models.IntegerField(blank=True, null=True)

    objects = PaymentManager()

    def __unicode__(self):
        return u"%s, %s, %s, %s" % (self.date, self.amount, self.user.username, self.method.name)

    class Meta:
        ordering = ['date']


class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return u"%s" % self.name


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
    fields=('date', 'amount', 'method')
    ordering=('date')

class MemberAdmin(admin.ModelAdmin):
    inlines=[ContactInfoInline, PaymentInfoInline, MembershipPeriodInline, PaymentInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


