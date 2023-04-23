from django.test import TestCase
from django.contrib.auth.models import User

from members.models import ContactInfo


class ContactInfoTest(TestCase):
    def test_get_date_of_entry_without_membership_period(self):
        user = User.objects.create()
        info = ContactInfo(user=user)
        info.get_date_of_first_join()  # does not raise
