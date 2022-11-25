from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load months collection CVS'
    args = "./manage.py import_payment absolute_filepath date(yyyy-mm-dd)"


    def add_arguments(self, parser):
        parser.add_argument('file')
        parser.add_argument('date', help='yyyy-mm-dd')

    def handle(self, *args, **options):
        from members.models import Payment

        print('importing')
        Payment.objects.import_smallfile(options['file'], options['date'])
        print('done')
