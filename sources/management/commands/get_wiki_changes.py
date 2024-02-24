from datetime import datetime

import feedparser
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from ...models import WikiChange


class Command(BaseCommand):
    help = 'Get the n most recent changes from the wiki.'

    def handle(self, *args, **options):
        feed = feedparser.parse(settings.MOS_WIKI_CHANGE_URL)

        # If there was _any_ kind of error, bail
        if 'bozo_exception' in feed:
            raise CommandError('Error parsing feed: %s' % feed['bozo_exception'])

        new_ids = []
        for entry in feed.entries[:settings.MOS_WIKI_KEEP]:
            o, _ = WikiChange.objects.get_or_create(
                    title=entry.title,
                    link=entry.link,
                    author=entry.author,
                    updated=datetime(*entry.updated_parsed[:6])
            )
            new_ids.append(o.id)

        # Keep only the newly added entries
        WikiChange.objects.exclude(id__in=new_ids).delete()
