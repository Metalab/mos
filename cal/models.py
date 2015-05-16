import datetime
import locale

from icalendar import Event as icalEvent
from icalendar.prop import vDatetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import permalink, Q

from mos.core.models import Category, Location
from mos.cal import create_calendar
import urllib
import sys

# We want our calendar to be displayed using the German locale
DESIRED_LOCALE = 'de_DE.UTF-8'

try:
    locale.setlocale(locale.LC_ALL, DESIRED_LOCALE)
except locale.Error:
    fallback_locale = locale.setlocale(locale.LC_ALL, '')
    print >>sys.stderr, """
    WARNING: Locale not found: %s
             Falling back to:  %s
    """ % (DESIRED_LOCALE, fallback_locale)


class EventManager(models.Manager):

    def get_queryset(self):
        return super(EventManager, self).get_queryset().filter(deleted=False)


class FutureEventFixedNumberManager(EventManager):

    def get_queryset(self):
        """
        Get <num> future events, or if there aren't enough,
        get <num> latest+future events.
        """

        DEFAULT_NUM = 5
        if(hasattr(settings, 'HOS_HOME_EVENT_NUM')):
            num = settings.HOS_HOME_EVENT_NUM
        else:
            num = DEFAULT_NUM

        return self.get_n(num)

    def get_n(self, num):

        all = super(FutureEventFixedNumberManager, self).get_queryset().order_by('startDate')

        if num == 0:
            return all

        future = all.filter(
            (Q(endDate__gte=datetime.datetime.now())) |
            (Q(endDate__isnull=True) &
             Q(startDate__gte=datetime.datetime.now() - datetime.timedelta(hours=5)))
        ).order_by('startDate')  # event visible 5 hours after it started

        if(future.count() < num):
            if(all.count() - num >= 0):
                latest = all[all.count() - num:all.count()]
            else:
                latest = all
        else:
            latest = future[:num]

        return latest


class Event(models.Model):
    """
    Represents an event
    """

    name = models.CharField(max_length=200)
    teaser = models.TextField(max_length=200, blank=True, null=True)
    wikiPage = models.CharField(max_length=200)

    startDate = models.DateTimeField()
    endDate = models.DateTimeField(blank=True, null=True)

    who = models.CharField(max_length=200, blank=True)
    where = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(default=datetime.datetime.now)
    created_by = models.ForeignKey(User)

    deleted = models.BooleanField(default=False)

    category = models.ForeignKey(Category, blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True)

    objects = models.Manager()
    all = EventManager()
    future = FutureEventFixedNumberManager()

    def __unicode__(self):
        status = ''
        if self.deleted:
            status = ' [deleted]'
        return u'%s (%s)%s' % (self.name, self.startDate, status)

    def past(self):
        return self.startDate < datetime.datetime.now()

    @permalink
    def get_absolute_url(self):
        return ('cal_event_detail', (self.id,),)

    def save(self, editor=False, new=False):
        if new and editor:
            self.created_by = editor
            self.created_by.save()

        super(Event, self).save()

    def start_end_date_eq(self):
        return self.startDate.date() == self.endDate.date()

    def delete(self):
        self.deleted = True

    def get_icalendar_event(self):
        domain = Site.objects.get_current().domain
        rv = icalEvent()

        rv.add('uid', u'%d@%s' % (self.id, domain))

        rv.add('summary', unicode(self.name))
        rv.add('dtstart', vDatetime(self.startDate).to_ical(), encode=0)
        rv.add('dtstamp', vDatetime(self.created_at).to_ical(), encode=0)
        rv.add('url', urllib.quote((u'http://%s/wiki/%s' % (domain, unicode(self.wikiPage))).encode('utf-8')) )

        if self.teaser:
            rv.add('description', unicode(self.teaser))

        if self.endDate:
            rv.add('dtend', vDatetime(self.endDate).to_ical(), encode=0)

        if self.who:
            rv.add('organizer', unicode(self.who))
        elif self.created_by_id and User.objects.filter(id=self.created_by_id):
            rv.add('organizer', unicode(self.created_by))

        if self.location:
            rv.add('location', u'Metalab ' + unicode(self.location))
        elif self.where:
            rv.add('location', u'Metalab ' + unicode(self.where))

        if self.category:
            rv.add('categories', unicode(self.category))

        return rv

    def get_icalendar(self):
        return create_calendar([self.get_icalendar_event()])

    @permalink
    def get_icalendar_url(self):
        return ('cal_event_icalendar', (self.id,))

