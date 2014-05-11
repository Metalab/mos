from django.test import TestCase
from django.contrib.auth.models import User

from mos.members.models import ContactInfo


class ContactInfoTest(TestCase):
    def test_get_date_of_entry_without_membership_period(self):
        user = User()
        info = ContactInfo(user=user)
        info.get_date_of_entry() # does not raise
