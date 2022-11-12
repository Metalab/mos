from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.template.loader import get_template
from cal.models import Event
import datetime
from django.utils.html import strip_tags
import requests


def get_next_jf():
    when = datetime.date.today() + datetime.timedelta(days=settings.MOS_JF_DAYS_IN_ADVANCE)
    try:
        return Event.objects.filter(category_id = settings.MOS_JF_DB_ID, startDate__date=when).first()
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

        text = heading["line"]

        if not text.startswith("Thema1") and not text.startswith("Thema2"):
            text = strip_tags(text)
            results.append(text)

    return {"article_missing": False, "error": len(results) == 0, "headlines": results}

def mail(template, ctx_vars):
    tpl = get_template(template)
    body = tpl.render(ctx_vars)
    subject = get_template(template + ".subject").render(ctx_vars).strip()
    send_mail(subject, body,
              settings.MOS_JF_SENDER,
              settings.MOS_JF_RECIPIENTS,
              fail_silently=False)

class Command(BaseCommand):
    help = 'Send the Jour Fixe reminder email, if a Jour Fixe is in settings.MOS_JF_DAYS_IN_ADVANCE days'

    def handle(self, *args, **kwargs):
        next_jf = get_next_jf()

        if next_jf:
            ctx = {'jf': next_jf, 'wiki': get_wiki_headlines(next_jf.wikiPage)}
            mail("jour_fixe_reminder.mail", ctx)
