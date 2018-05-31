from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, MONTHLY
from django.contrib.auth.models import User

from .models import MembershipPeriod


def get_date_of_entry(user):
    mp_list = MembershipPeriod.objects.filter(user__exact=user).order_by('begin')[:1]
    if len(mp_list) < 1:
        return None
    return mp_list[0].begin


def get_date_of_exit(user):
    mp_list = MembershipPeriod.objects.filter(user__exact=user).order_by('-begin')[:1]
    if len(mp_list) < 1:
        return None
    return mp_list[0].end


class HistoryEntry:
    month = date.today()
    num_member = 0
    new_member = 0
    resigned_member = 0


def get_list_of_history_entries():
    end_of_month = date.today() + relativedelta(day=31)

    he_list = {}
    month_list = rrule(MONTHLY, dtstart=date(2006, 3, 1), until=end_of_month)
    for month in month_list:
        d = date(month.year, month.month, month.day)
        he_list[d] = HistoryEntry()
        he_list[d].month = d

    for u in User.objects.all():
        mps = u.membershipperiod_set.values_list('begin', 'end')
        if not mps:
            continue

        starts, ends = zip(*mps)
        starts = list(starts) + [None]
        ends = [None] + list(ends)

        for end, start in zip(ends, starts):
            if end is None and start is None:
                continue

            if end is None:
                he_list[start.replace(day=1)].new_member += 1
                continue

            if start is None:
                if end <= end_of_month:
                    he_list[end.replace(day=1)].resigned_member += 1
                continue

            pause = start.replace(day=1) - (end + relativedelta(day=31))
            if pause > timedelta(1):
                he_list[start.replace(day=1)].new_member += 1
                if end <= end_of_month:
                    he_list[end.replace(day=1)].resigned_member += 1

    num = 0
    for month in month_list:
        he = he_list[month.date()]
        num += he.new_member
        num -= he.resigned_member
        he.num_member = num

    return he_list


def generate_bank_collection_list(for_month):
    member_list = Member.objects.all()
    for_month = date(for_month.year, for_month.month, 1)
    list = {}
    for member in member_list:
        if member.bank_collection_allowed:
            fee = member.get_membership_fee(for_month)
            if fee is not None and fee.amount > 0:
                list[member] = fee.amount

    return list
