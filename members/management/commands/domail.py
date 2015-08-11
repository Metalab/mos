from __future__ import print_function

from django.core.management.base import BaseCommand

from members.models import get_active_members


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for user in get_active_members():
            user.is_active = True
            user.save()

            print(user, user.email)
