from django.contrib.syndication.feeds import Feed
from models import Event
import datetime


class EventFeed(Feed):
    title=u'Zukuenftige Veranstaltungen'
    link='/'
    description=u'''zukuenftige Veranstaltungen in und um den Wiener
                  Hackerspace Metalab'''

    def items(self):
        return Event.all.filter(startDate__gte=datetime.datetime.now()).\
            order_by('startDate')
