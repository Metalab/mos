from __future__ import print_function

from django.core.management.base import LabelCommand
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth import get_user_model
from django.db.models import Q

from datetime import date

from ...models import get_active_members_for


class Command(LabelCommand):
    help = "My shiny new management command."

    def handle_label(self, label, **options):
        year = int(label)
        
        print('        normal klein 2*klein ohne insg.')
        for month in range(1, 13):
            dt = date(year, month, 1)
            counts = self.handle_date(dt)
            print(dt.strftime('%m/%Y'), '%4d%6d%7d%7d' % counts, ' ', sum(counts))

    def handle_date(self, dt):
        User = get_user_model()

        count_normal, count_small, count_2small, count_without = 0, 0, 0, 0
        for user in get_active_members_for(dt):
            # we have to get first() because the last day of one period
            # may be the same as the first day of the next period.
            # this shouldn't happen, but oh well...
            # also get_active_members_for uses begin <= dt <= end
            period = user.membershipperiod_set.filter(
                    Q(begin__lte=dt),
                    Q(end__isnull=True) | Q(end__gte=dt)
            ).first()

            # please do not  implement this, like we did /o\
            # strings für normale Spinde
            normal_locker = ['normal+spind', 'free+spind',
                'ermäßigt (7EUR) + Spind', 'Erhöht (35EUR) + Spind']

            # strings für kleine  Spinde
            small_locker = ['normal + kleiner Spind', 'free + kleiner Spind',
                'ermäßigt (7EUR) + kl. Spind', 'ermäßigt (15EUR) + kl. Spind']

            # strings für 2 kleine  Spinde
            two_small_lockers = ['normal + 2 kleine Spinde']

            kind = period.kind_of_membership.name
            if kind in normal_locker:
                count_normal += 1
            elif kind in small_locker:
                count_small += 1
            elif kind in two_small_lockers:
                count_2small += 1
            else:
                count_without += 1
        return count_normal, count_small, count_2small, count_without
