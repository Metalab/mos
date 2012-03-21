from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from optparse import make_option
import sys
import os

try:
    set
except NameError:
    from sets import Set as set   # Python 2.3 fallback

class Command(BaseCommand):
    help = 'Load months collection CVS'
    args = "./manage.py import_payment absolute_filepath date(yyyy-mm-dd)"

    def handle(self, *args, **kwargs):
        from django.db.models import get_apps
        from django.core import serializers
        from django.db import connection, transaction
        from django.conf import settings
        from mos.members.models import Payment

        if len(args)!=2:
            print self.help
            print self.args
            return

        file = args[0]
        date = args[1]

        print 'importing'
        Payment.objects.import_smallfile(file, date)
        print 'done'      
