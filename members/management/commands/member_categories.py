from __future__ import print_function

from django.core.management.base import LabelCommand
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth import get_user_model
from django.db.models import Q

from datetime import date

from ...models import get_active_members_for

from collections import defaultdict


class Command(LabelCommand):
    help = "My shiny new management command."

    def handle_label(self, label, **options):
        year = int(label)

        print(f'Mitgliedskategorien je Monat im Jahr {year}:')
        for month in range(1, 13):
            dt = date(year, month, 1)
            data_dict, sum_users = self.handle_date(dt)
            print(dt.strftime('%m/%Y'), 'Member in Summe:', sum_users)
            for key, value in data_dict.items():
                print(key, value)

        print("\n")

    def handle_date(self, dt):
        member_category_dict = defaultdict(int)
        user_sum = 0
        for user in get_active_members_for(dt):
            # we have to get first() because the last day of one period
            # may be the same as the first day of the next period.
            # this shouldn't happen, but oh well...
            # also get_active_members_for uses begin <= dt <= end
            period = user.membershipperiod_set.filter(
                    Q(begin__lte=dt),
                    Q(end__isnull=True) | Q(end__gte=dt)
            ).first()

            member_category_dict[period.kind_of_membership.name] += 1
            user_sum += 1

        return member_category_dict, user_sum
