import datetime

from django.test import TestCase
from freezegun import freeze_time

from members.models import MembershipPeriod


class MembershipPeriodTest(TestCase):
    def test_get_duration_takes_max_year(self):
        period = MembershipPeriod(
                    begin=datetime.date(2000, 1, 1),
                    end=datetime.date(9999, 12, 31)
                 )
        period.get_duration_in_month()  # should not raise

    def test_get_duration_handles_future_end_date(self):
        with freeze_time('2000-05-10'):
            period = MembershipPeriod(
                        begin=datetime.date(2000, 5, 1),
                        end=datetime.date(3000, 5, 1)
                     )
            self.assertEqual(period.get_duration_in_month(), 1)
