import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template.loader import get_template

from things.models import ThingUser


def mail(template, ctx_vars, recipient):
    tpl = get_template(template)
    body = tpl.render(ctx_vars)
    subject = get_template(template + ".subject").render(ctx_vars).strip()
    send_mail(
        subject, body, settings.HOS_ANNOUNCE_FROM, [recipient], fail_silently=False
    )


class Command(BaseCommand):
    help = "Send thing expiration reminder to all members whose thing expires 1 month from now"

    def handle(self, *args, **options):
        expiring_thing_users = ThingUser.objects.filter(
            best_before__lte=datetime.date.today() + datetime.timedelta(days=31),
            best_before__gt=datetime.date.today() + datetime.timedelta(days=30),
        )

        for expiring_thing in expiring_thing_users:
            ctx = {
                "user": expiring_thing.user,
                "thing": expiring_thing.thing,
                "expiry_date": expiring_thing.best_before,
                "expiry_notice": expiring_thing.thing.expiry_notice,
            }
            mail("things/thing_expiration_notice.mail", ctx, expiring_thing.user.email)
