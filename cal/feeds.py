from __future__ import unicode_literals

import datetime

from django.contrib.syndication.views import Feed
from django.db.models import Q

from .models import Event


class EventFeed(Feed):
    title = 'Zukuenftige Veranstaltungen'
    link = '/'
    description = 'zukuenftige und laufende Veranstaltungen ' \
                  'in und um den Wiener Hackerspace Metalab'

    def items(self):
        now = datetime.datetime.now()
        future = Q(startDate__gte=now)
        running = Q(startDate__lte=now) & Q(endDate__gte=now)
        return Event.all.filter(future|running).order_by('startDate')
