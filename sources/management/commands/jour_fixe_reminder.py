import datetime

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template.loader import get_template

from cal.models import Event


def get_next_jf():
    return Event.objects.filter(pk=2317).first()
    when = datetime.date.today() + datetime.timedelta(days=settings.MOS_JF_DAYS_IN_ADVANCE)
    try:
        return Event.objects.filter(category_id = settings.MOS_JF_DB_ID, startDate__date=when).first()
    except ObjectDoesNotExist:
        return None

def get_wiki_headlines(article):
    response = requests.get(settings.HOS_WIKI_FULL_URL + article)

    if not response.ok:
        return {"article_missing": True, "error": True, "headlines": []}

    article = BeautifulSoup(response.content, 'html.parser')
    in_themen_heading = False
    results = []

    for heading in article.select("h1,h2"):
        try:
            headline = heading.select(".mw-headline")[0].get_text()
        except IndexError:
            continue

        if heading.name == "h1":
            if in_themen_heading:
                break
            if headline == "Themen":
                in_themen_heading = True
                continue
        elif in_themen_heading and not headline.startswith("Thema1") and not headline.startswith("Thema2"):
            results.append(headline)

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
