from django.core.management.base import BaseCommand

from members.models import get_mailinglist_members
from members.models import MailinglistMail


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        members_on_intern = get_mailinglist_members().filter(contactinfo__on_intern_list=True)
        addresses = [x.contactinfo.intern_list_email for x
            in members_on_intern
            if x.contactinfo.intern_list_email != '']
        addresses.extend(
            e.email
            for e in MailinglistMail.objects.filter(on_intern_list=True)
        )
        print('\n'.join(addresses))
