from mos.members.models import *
from django.contrib.auth.models import User
from datetime import *
from dateutil.rrule import *


def get_date_of_entry(user):
    mp_list = MembershipPeriod.objects.filter(user__exact=user)\
              .order_by('begin')[:1]
    if len(mp_list) < 1:
        return None
    return mp_list[0].begin


def get_date_of_exit(user):
    mp_list = MembershipPeriod.objects.filter(user__exact=user)\
              .order_by('-begin')[:1]
    if len(mp_list) < 1:
        return None
    return mp_list[0].end


class HistoryEntry:
    month = date.today()
    num_member = 0
    new_member = 0
    resigned_member = 0


def get_list_of_history_entries():
    he_list = {}

    month_list = list(rrule(MONTHLY, dtstart=date(2006, 3, 1),
                            until=date.today()))
    for month in month_list:
        d = date(month.year, month.month, month.day)
        he_list[d] = HistoryEntry()
        he_list[d].month = d

    user_list = User.objects.all()
    for u in user_list:
        entry = get_date_of_entry(u)
        entry = date(entry.year, entry.month, 1)
        num = he_list[entry].new_member
        num += 1
        he_list[entry].new_member = num

        end = get_date_of_exit(u)
        if end is not None:
            end = date(end.year, end.month, 1)
            num = he_list[end].resigned_member
            num += 1
            he_list[end].resigned_member = num

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
