import datetime
from django.core.management.base import BaseCommand
from django.db import transaction

from dateutil.relativedelta import relativedelta
from ...models import PaymentMethod, User
from ...models import ContactInfo
from ...models import KindOfMembership
from ...models import Payment
from ...models import MembershipPeriod


class Command(BaseCommand):
    help = 'Generate a lot of members for testing'
    args = "./manage.py import_payment absolute_filepath date(yyyy-mm-dd)"


    def add_arguments(self, parser):
        parser.add_argument('--number-of-members', type=int, required=True)
        parser.add_argument('--memberships-per-member', type=int, required=True)

    @transaction.atomic
    def handle(self, number_of_members, memberships_per_member, *args, **options):
        for member_num in range(number_of_members):
            user = User.objects.filter(username=f"member{member_num}").delete()
            user = User.objects.create(username=f"member{member_num}")

            info = ContactInfo.objects.create(
                user=user,
            )

            start_date = datetime.datetime(1960, 1, 1)

            kind_of_membership = KindOfMembership.objects.first()
            fee = kind_of_membership.membershipfee_set.first()
            fee.start = start_date
            fee.save()

            for _ in range(memberships_per_member):
                new_start_date = start_date + relativedelta(months=1)
                MembershipPeriod.objects.create(
                    begin=start_date,
                    end=new_start_date,
                    user=user,
                    kind_of_membership=kind_of_membership,
                )
                Payment.objects.create(
                    date=start_date + relativedelta(days=3),
                    user=user,
                    amount=10,
                    method=PaymentMethod.objects.first(),
                )
                start_date = new_start_date

            MembershipPeriod.objects.create(
                begin=new_start_date,
                user=user,
                kind_of_membership=kind_of_membership,
            )
