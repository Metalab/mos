import sys
import urllib.parse
import datetime
import locale

from icalendar import Event as icalEvent
from icalendar.prop import vDatetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import Q
from django.urls import reverse

from core.models import Category, Location
from . import create_calendar

# We want our calendar to be displayed using the German locale
DESIRED_LOCALE = 'de_DE.UTF-8'

try:
    locale.setlocale(locale.LC_ALL, DESIRED_LOCALE)
except locale.Error:
    fallback_locale = locale.setlocale(locale.LC_ALL, '')
    print("""WARNING: Locale not found: %s
             Falling back to:  %s
    """ % (DESIRED_LOCALE, fallback_locale), file=sys.stderr)


class EventQuerySet(models.QuerySet):
    pass


class EventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class FutureEventFixedNumberManager(EventManager):
    def get_queryset(self):
        """
        Get <num> future events, or if there aren't enough,
        get <num> latest+future events.
        """
        num = getattr(settings, 'HOS_HOME_EVENT_NUM', 5)
        return self.get_n(num)

    def get_n(self, num, past_duration=datetime.timedelta(hours=5)):
        all = super().get_queryset().order_by('startDate')

        if num == 0:
            return all

        future = all.filter(
            (Q(endDate__gte=datetime.datetime.now())) |
            (Q(endDate__isnull=True) &
             Q(startDate__gte=datetime.datetime.now() - past_duration))
        ).order_by('startDate')  # event visible X hours/days/weeks/... after it started

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
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    advertise = models.BooleanField(default=False)

    deleted = models.BooleanField(default=False)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    objects = EventQuerySet.as_manager()
    all = EventManager.from_queryset(EventQuerySet)()
    future = FutureEventFixedNumberManager.from_queryset(EventQuerySet)()

    def __str__(self):
        status = ''
        if self.deleted:
            status = ' [deleted]'
        return '%s (%s)%s' % (self.name, self.startDate, status)

    def past(self):
        if self.endDate:
            return self.endDate < datetime.datetime.now()
        else:
            return self.startDate < datetime.datetime.now()

    def get_absolute_url(self):
        return reverse('cal_event_detail', args=(self.id,))

    def save(self, editor=False, new=False):
        if new and editor:
            self.created_by = editor
            self.created_by.save()

        super().save()

    def start_end_date_eq(self):
        return self.startDate.date() == self.endDate.date()

    def delete(self, commit=True):
        self.deleted = True
        if commit:
            self.save()

    def get_icalendar_event(self):
        domain = Site.objects.get_current().domain
        rv = icalEvent()

        rv.add('uid', '%d@%s' % (self.id, domain))

        rv.add('summary', self.name)
        rv.add('dtstart', vDatetime(self.startDate).to_ical(), encode=0)
        rv.add('dtstamp', vDatetime(self.created_at).to_ical(), encode=0)
        rv.add('url', 'https://{}/wiki/{}'.format(domain, urllib.parse.quote(self.wikiPage)))

        if self.teaser:
            rv.add('description', self.teaser)

        if self.endDate:
            rv.add('dtend', vDatetime(self.endDate).to_ical(), encode=0)

        if self.who:
            rv.add('organizer', self.who)
        elif self.created_by_id and User.objects.filter(id=self.created_by_id):
            rv.add('organizer', self.created_by)

        if self.location:
            rv.add('location', 'Metalab %s' % self.location)
        elif self.where:
            rv.add('location', 'Metalab %s' % self.where)

        if self.category:
            rv.add('categories', self.category)

        return rv

    def get_icalendar(self):
        return create_calendar([self.get_icalendar_event()])

    def get_icalendar_url(self):
        return reverse('cal_event_icalendar', args=(self.id,))
