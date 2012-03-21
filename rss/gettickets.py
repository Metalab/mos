#!/usr/bin/python
import sys, os
import datetime
import feedparser

sys.path.append('/django/svn/trunk/')
sys.path.append('/django/deployment/')
os.environ['DJANGO_SETTINGS_MODULE'] = "mos.settings"

from django.conf import settings

from mos.rss.models import Change


d = feedparser.parse(settings.HOS_WIKI_CHANGE_URL)

for x in d.entries:

    updated = datetime.datetime(*x.updated_parsed[0:6])

    preexisting = Change.objects.filter(title=x.title, link=x.link,
                                        author=x.author, updated=updated)

    if len(preexisting) > 0:
        continue

    change = Change(title=x.title, link=x.link, author=x.author,
                    updated=updated)
    change.save()
