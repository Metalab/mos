from __future__ import print_function

import csv

from django.core.management.base import BaseCommand

from members.models import Payment, PaymentInfo, PaymentMethod


(ERROR, FIRST_NAME, LAST_NAME, ACCOUNT_NUMBER, BANK_CODE, FULL_NAME,
    AMOUNT, TEXT, IBAN, BIC, MANDATE_REFERENCE, DATE, F1, F2) = range(14)

FIELDS = (ERROR, FIRST_NAME, LAST_NAME, ACCOUNT_NUMBER, BANK_CODE, FULL_NAME,
          AMOUNT, TEXT, IBAN, BIC, MANDATE_REFERENCE, DATE, F1, F2)


class Command(BaseCommand):
    help = 'Load months collection CVS'
    args = "./manage.py import_payment absolute_filepath"

    def reader(self):
        with open(self.file) as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=FIELDS, delimiter=';', strict=True)
            for row in reader:
                yield row

    def handle(self, *args, **kwargs):
        if len(args) != 1:
            print(self.help)
            print(self.args)
            return

        self.file = args[0]

        payment_method = PaymentMethod.objects.get(name='bank collection')

        for line in self.reader():
            if line[ERROR].startswith('#'):
                print(line[ERROR])
                continue

            if all(v=='' for v in line.values()):
                continue

            mandata_reference = line[MANDATE_REFERENCE]
            info = PaymentInfo.objects.get(bank_account_mandate_reference=mandata_reference)
            user = info.user

            payment = Payment.objects.create(
                amount=line[AMOUNT],
                date=line[DATE],
                method=payment_method,
                user=user,
                original_line='',
                original_file=self.file,
                original_lineno=0)
