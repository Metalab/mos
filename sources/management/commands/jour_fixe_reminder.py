from django.core.management.base import NoArgsCommand, CommandError
from django.conf import settings
import datetime
from cal.models import Event
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context

# TODO: does this handle timezones correctly?
# TODO: send a warning mail to core if the next jour fixe does not have a wiki page
# TODO: download and parse the wiki page and add the summary to the reminder mail

def get_next_jf():
    when = datetime.date.today() + datetime.timedelta(days = settings.MOS_JF_DAYS_IN_ADVANCE)
    try:
        # FIXME: django too old, this doesn't work yet: startDate__date = when
        return Event.objects.get(category_id = settings.MOS_JF_DB_ID,
                                 startDate__year  = when.year,
                                 startDate__month = when.month,
                                 startDate__day   = when.day)
    except MultipleObjectsReturned as e:
        # Ehhhhh. Multiple Jour fixes in the calendar for the same date.
        raise e # FIXME send warning email
    except ObjectDoesNotExist:
        return None

def mail(template, ctx_vars):
    tpl = get_template(template)
    ctx = Context(ctx_vars)
    msg = tpl.render(ctx)
    sub = ''.join(get_template(template + ".subject").render(ctx).splitlines())
    send_mail(sub, msg,
              settings.MOS_JF_SENDER,
              settings.MOS_JF_RECIPIENTS,
              fail_silently=False)

def debug():
    import pdb
    pdb.set_trace()

class Command(NoArgsCommand):
    help = 'Send the Jour Fixe reminder email, if a Jour Fixe is in settings.MOS_JF_DAYS_IN_ADVANCE days'
    def handle_noargs(self, **options):
        next_jf = get_next_jf()
        if not next_jf:
            return
        mail("jour_fixe_reminder.mail", { 'jf': next_jf })
