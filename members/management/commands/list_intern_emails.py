from django.core.management.base import BaseCommand

from members.models import get_mailinglist_members


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        members_on_intern = get_mailinglist_members().filter(contactinfo__on_intern_list=True)
        addresses = [x.contactinfo_set.all()[0].intern_list_email for x
            in members_on_intern
            if x.contactinfo_set.all()[0].intern_list_email != '']

        print '\n'.join(addresses)
