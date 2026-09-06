import datetime

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template.loader import get_template

from cal.models import Event


def get_next_exclusive_day():
    when = datetime.date.today() + datetime.timedelta(days=settings.MOS_EXCLUSIVE_DAYS_DAYS_IN_ADVANCE)
    try:
        return Event.objects.filter(category_id = settings.MOS_EXCLUSIVE_DAYS_DB_ID, startDate__date=when).first()
    except ObjectDoesNotExist:
        return None

def mail(template, ctx_vars):
    tpl = get_template(template)
    body = tpl.render(ctx_vars)
    subject = get_template(template + ".subject").render(ctx_vars).strip()
    send_mail(subject, body,
              settings.MOS_EXCLUSIVE_DAYS_SENDER,
              settings.MOS_EXCLUSIVE_DAYS_RECIPIENTS,
              fail_silently=False)

class Command(BaseCommand):
    help = 'Send the reminder email for the next exclusive day, if an exclusive day is in settings.MOS_EXCLUSIVE_DAYS_DAYS_IN_ADVANCE days'

    def handle(self, *args, **kwargs):
        next_exclusive_day = get_next_exclusive_day()

        if next_exclusive_day:
            ctx = {'ed': next_exclusive_day}
            mail("exclusive_day_reminder.mail", ctx)
