from __future__ import print_function

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load months collection CVS'
    args = "./manage.py import_payment absolute_filepath date(yyyy-mm-dd)"

    def handle(self, *args, **kwargs):
        from django.conf import settings
        from members.models import Payment

        if len(args) != 2:
            print(self.help)
            print(self.args)
            return

        file = args[0]
        date = args[1]

        print('importing')
        Payment.objects.import_smallfile(file, date)
        print('done')
