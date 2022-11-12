from __future__ import absolute_import
import datetime

from django.urls import path, re_path
from django.views.generic.dates import YearArchiveView
from django.views.generic.detail import DetailView
from functools import partial

from .models import Event, Location, Category
import cal.views


date_dict = {
    'queryset': Event.all.all(),
    'date_field': 'startDate',
    'allow_future': True,
}

archive_index_dict = date_dict.copy()
archive_index_dict.update(
    num_latest=100,
    template_object_name='latestevents',
    allow_empty=True,
)

event_detail_dict = date_dict.copy()
event_detail_dict.update(template_object_name='event')


urlpatterns = [
    path(
        '',
        cal.views.index,
        {},
        'cal_index',
    ),
    re_path(
        r'^(?P<year>\d{4})/$',
        YearArchiveView.as_view(
            queryset=Event.all.all(),
            date_field="startDate",
            allow_future=True,
            make_object_list=True,
        ),
        {},
        "cal_archive_year",
    ),
    re_path(
        r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        cal.views.monthly,
    ),
    re_path(
        r'^special/(?P<typ>\w+)/(?P<name>\w+)/$',
        cal.views.display_special_events,
    ),
    re_path(
        r'^event/(?P<pk>\d+)/$',
        DetailView.as_view(
            queryset=Event.all.all(),
            context_object_name='event',
        ),
        {},
        'cal_event_detail',
    ),
    re_path(
        r'^event/(?P<object_id>\d+)/update/$',
        cal.views.update_event,
        { 'new': False },
    ),
    re_path(
        r'^(?P<object_id>\d+)/update/$',
        cal.views.update_event,
        { 'new': False },
    ),
    re_path(
        r'^event/(?P<object_id>\d+)/delete/',
        cal.views.delete_event,
    ),
    re_path(
        r'^(?P<object_id>\d+)/delete/',
        cal.views.delete_event,
    ),
    re_path(
        r'^event/(?P<object_id>\d+)/icalendar/',
        cal.views.event_icalendar,
        {},
        'cal_event_icalendar',
    ),
    path(
        'export/ical/',
        partial(cal.views.complete_ical, num=100, past_duration=datetime.timedelta(days=7)),
        {},
        'small_ical',
    ),
    path(
        'export/ical_full/',
        partial(cal.views.complete_ical, num=0, past_duration=None),
        {},
        'full_ical',
    ),
    path(
        'event/new/',
        cal.views.update_event,
        { 'new': True },
    ),
    path(
        'new/',
        cal.views.update_event,
        { 'new': True },
    ),
    path(
        'locations/',
        cal.views.SpecialListView.as_view(
            queryset=Location.objects.all(),
            events_by="Locations",
        ),
    ),
    path(
        'categories/',
        cal.views.SpecialListView.as_view(
            queryset=Category.objects.all(),
            events_by="Categories",
        ),
    ),
    re_path(
        r'^ajax/list/(?P<number>\d*)/?$',
        cal.views.event_list,
    ),
]
