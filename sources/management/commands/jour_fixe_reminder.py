from django.core.management.base import NoArgsCommand, CommandError
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from cal.models import Event
import datetime, requests

# TODO: does this handle timezones correctly?
# TODO: send a warning mail to core if the next jour fixe does not have a wiki page

def get_next_jf():
    when = datetime.date.today() + datetime.timedelta(days = settings.MOS_JF_DAYS_IN_ADVANCE)
    try:
        # FIXME: django too old, this doesn't work yet: startDate__date = when
        return Event.objects.get(category_id = settings.MOS_JF_DB_ID,
                                 startDate__year  = when.year,
                                 startDate__month = when.month,
                                 startDate__day   = when.day)
    except MultipleObjectsReturned as e:
        raise e # FIXME: Ehhhhh. Multiple Jour fixes in the calendar for the same date.
    except ObjectDoesNotExist:
        return None

def get_wiki_article(article):
    query = {"action": "parse", "page": article, "format": "json"}
    return requests.get(settings.MEDIAWIKI_API, params = query).json()

def get_wiki_headlines(article):
    article = get_wiki_article(article)
    if article.get("error", False):
        return {"article_missing": True, "error": True, "headlines": []}

    results = []
    skip = True
    for heading in article["parse"]["sections"]:
        if heading["toclevel"] == 1:
            skip = heading["anchor"] != "Themen"
            continue
        if skip:
            continue
        results.append(heading["line"])

    return {"article_missing": False, "error": len(results) == 0, "headlines": results}

def mail(template, ctx_vars):
    tpl = get_template(template)
    ctx = Context(ctx_vars)
    msg = tpl.render(ctx)
    sub = ''.join(get_template(template + ".subject").render(ctx).splitlines())
    send_mail(sub, msg,
              settings.MOS_JF_SENDER,
              settings.MOS_JF_RECIPIENTS,
              fail_silently=False)

class Command(NoArgsCommand):
    help = 'Send the Jour Fixe reminder email, if a Jour Fixe is in settings.MOS_JF_DAYS_IN_ADVANCE days'
    def handle_noargs(self, **options):
        next_jf = get_next_jf()
        if not next_jf:
            return
        ctx = { 'jf': next_jf, 'wiki': get_wiki_headlines(next_jf.wikiPage) }
        mail("jour_fixe_reminder.mail", ctx)
