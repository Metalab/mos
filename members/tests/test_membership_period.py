import datetime
import contextlib

from django.test import TestCase

from mos.members.models import MembershipPeriod


@contextlib.contextmanager
def mock_date(fake_date):
    """Context manager for mocking out datetime.date.today() in unit tests.

    Example:
    with mock_date(datetime.date(2011, 2, 3)):
        assert datetime.date.today() == datetime.date(2011, 2, 3)
    """

    class MockDate(datetime.date):
        @classmethod
        def today(cls):
            # Create a copy of fake_date.
            return datetime.date(fake_date.year, fake_date.month, fake_date.day)
    real_date = datetime.date
    datetime.date = MockDate
    try:
        yield datetime.date
    finally:
        datetime.date = real_date


class MembershipPeriodTest(TestCase):
    def test_get_duration_takes_max_year(self):
        period = MembershipPeriod(
                    begin = datetime.date(2000, 1, 1),
                    end = datetime.date(9999, 12, 31)
                 )
        period.get_duration_in_month() # should not raise

    def test_get_duration_handles_future_end_date(self):
        with mock_date(datetime.date(2000, 5, 10)):
            period = MembershipPeriod(
                        begin = datetime.date(2000, 5, 1),
                        end = datetime.date(3000, 5, 1)
                     )
            self.assertEqual(period.get_duration_in_month(), 1)
