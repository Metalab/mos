import json
import urllib.parse
from calendar import HTMLCalendar
from calendar import month_name
from datetime import date

from dateutil import relativedelta
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from django.utils.html import conditional_escape as esc
from django.utils.safestring import mark_safe

from . import create_calendar
from .forms import EventForm
from .models import Category
from .models import Event
from .models import Location


class EventCalendar(HTMLCalendar):

    def __init__(self, events, admin=False):
        super().__init__()
        self.events = events
        self.admin = admin

    def formatday(self, day, weekday):
        if day != 0:
            # self.year and self.month are set as a side-effect of formatmonth()
            this_day = date(self.year, self.month, day)

            next_day = this_day + relativedelta.relativedelta(days=1)
            day_events = (
                self.events
                .exclude(startDate__gte=next_day)
                .exclude(endDate__lt=this_day, endDate__isnull=False)
                .exclude(endDate__isnull=True, startDate__lt=this_day)
            )
            cssclass = self.cssclasses[weekday]
            if date.today() == this_day:
                cssclass += ' today'
                cssclass += ' filled'
            if day_events.filter(category__slug="exklusiver_tag").exists():
                cssclass += ' exklusiver_tag'
            body = ['<ul class="daily-events">']
            for event in day_events:
                start_day = event.startDate.date()
                end_day = (event.endDate or event.startDate).date()

                body.append('<li class="event">')
                if self.admin:
                    body.append(u'<a href="%s" class="edit" title="edit">✏️</a>' % event.get_absolute_url())
                body.append('<a href="/wiki/%s">' % esc(event.wikiPage))
                if this_day == start_day:
                    body.append('<span class="event-time">' + event.startDate.strftime('%H:%M') + '</span>')
                body.append('<span class="event-name">' + esc(event.name) + '</span>')
                if start_day != end_day and this_day == end_day:
                    body.append(' <span class="event-time">' + event.endDate.strftime('%H:%M') + '</span>')
                body.append('<span class="event-location">' + esc(event.location) + '</span>')
                body.append('</a>')
                body.append('</li>')
            body.append('</ul>')
            return self.day_cell(cssclass, '%d %s' % (day, (''.join(body))))

            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        # Remember year and month for use in formatday()
        self.year, self.month = year, month
        return super().formatmonth(year, month)

    def formatmonthname(self, theyear, themonth, withyear=True):
        # Adapted from Python's Lib/calendar.py

        if withyear:
            s = '%s %s' % (month_name[themonth], theyear)
        else:
            s = '%s' % month_name[themonth]

        d = date(int(theyear), int(themonth), 1)

        # Any date before 1 or past 9999 crashes. Make sure we don't try to calculate such a date.
        try:
            prev = d - relativedelta.relativedelta(months=1)
            prevLink = f'<a href="/calendar/{prev.year:04d}/{prev.month:02d}/">&lt;</a>'
        except ValueError:
            prevLink = ''

        try:
            next = d + relativedelta.relativedelta(months=1)
            nextLink = f'<a href="/calendar/{next.year:04d}/{next.month:02d}/">&gt;</a>'
        except ValueError:
            nextLink = ''

        return f'''
        <tr><th colspan="7" class="{self.cssclass_month_head}">
            {prevLink}
            {s}
            {nextLink}
        </th></tr>'''

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

    def currentmonth(self):
        t = date.today()
        return self.formatmonth(t.year, t.month)


def all(request):
    d = date.today() - relativedelta.relativedelta(days=2)
    cal = EventCalendar(Event.all.order_by('startDate'), request.user.is_authenticated).currentmonth()
    date_list = Event.all.all().datetimes('startDate', 'year')
    latest_events = Event.all.filter(startDate__gte=d).order_by('startDate')

    return render(request, 'cal/event_archive.html', {
        'rendered_calendar': mark_safe(cal),
        'date_list': date_list,
        'latestevents': latest_events
    })

def index(request):
    d = date.today()
    return monthly(request, d.year, d.month)

def monthly(request, year, month):
    try:
        s = date(int(year), int(month), 1)
    except ValueError:
        raise Http404

    e = date(int(year), int(month), 1) + relativedelta.relativedelta(months=1)
    latest_events = Event.all.filter(startDate__gte=s, startDate__lt=e).order_by('startDate')
    cal = EventCalendar(Event.all.order_by('startDate'), request.user.is_authenticated).formatmonth(int(year), int(month))
    date_list = Event.all.all().datetimes('startDate', 'year')

    return render(request, 'cal/event_archive.html', {
        'rendered_calendar': mark_safe(cal),
        'date_list': date_list,
        'latestevents': latest_events
    })


def display_special_events(request, typ, name):
    """
    Displays special events by location or category
    """

    try:
        if typ == 'Category':
            events = Event.objects.filter(category__name=name)
            des = get_object_or_404(Category, name=name)
        elif typ == 'Location':
            events = Event.objects.filter(location__name=name)
            des = get_object_or_404(Location, name=name)
        else:
            events = None
            des = None

    except ObjectDoesNotExist:
        events = None

    return render(request, 'cal/event_archive.html', {
        'latestevents': events,
        'title': name,
        'type': typ,
        'description': des,
    })


@login_required
def delete_event(request, object_id=None):
    if not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    event = get_object_or_404(Event.all, id=object_id)

    event.delete()

    return HttpResponse()


@login_required
def update_event(request, new, object_id=None):
    if not new:
        event = get_object_or_404(Event.all, id=object_id)
    else:
        event = Event()

    event_valid = True

    if request.method == 'POST':
        event_form = EventForm(request.POST, instance=event)

        if event_form.is_valid():
            event_data = event_form.save(commit=False)
            event_data.save(request.user, new)
            event = Event.objects.get(id=event_data.id)
        else:
            event_valid = False
    else:
        event_form = EventForm()

    response = render(request, 'cal/eventinfo_nf.inc', {
        'event_has_error': not event_valid,
        'event_form': event_form,
        'event': event,
        'new': not event.pk,
    })

    if not event_valid:
        response.status_code = 500

    return response


def event_list(request, number=0):
    events = Event.future.get_n(int(number) if number != '' else 0)

    if not number:
        events = events.reverse()

    return render(request, 'cal/calendar.inc',
                              {'latestevents': events})


def event_icalendar(request, object_id):
    event = get_object_or_404(Event.all, pk=object_id)

    response = HttpResponse(event.get_icalendar().to_ical(),
                        content_type='text/calendar; charset=utf-8')

    response['Content-Disposition'] = 'filename="{}-{}.ics"'.format(event.startDate.strftime('%Y-%m-%d'), event.name)

    return response


def complete_ical(request, num, past_duration):
    events = Event.future.get_n(num, past_duration)

    if not num:
        events = events.reverse()

    calendar = create_calendar([x.get_icalendar_event() for x in events])
    return HttpResponse(calendar.to_ical(), content_type='text/calendar; charset=utf-8')

def public_upcoming(request):
    events = Event.objects.not_deleted().advertise().filter(
        endDate__gte=timezone.now().date(),
    ).order_by("startDate", "pk")[:5]

    data = []
    for event in events:
        sd = event.startDate
        ed = event.endDate

        # Date format examples:
        # Wed 30.11.2022 19:00 - 23:00
        # Fri 25.11.2022 18:30 - 18:30 (+2)
        # Date and times
        date_formatted = f"{sd:%a %d.%m.%Y %H:%M} - {ed:%H:%M}"

        # Day offset suffix if needed
        if (days_diff := (ed.date() - sd.date()).days) > 0:
            date_formatted += f" (+{days_diff})"

        event_data = {
            "date": date_formatted,
            "title": event.name,
            "url": f"https://metalab.at/wiki/{urllib.parse.quote(event.wikiPage)}",
            "subtitle": event.teaser,
        }
        data.append(event_data)

    return HttpResponse(json.dumps(data), content_type="application/json")
