from __future__ import absolute_import

from django.conf.urls import *
from django.views.generic.dates import YearArchiveView
from django.views.generic.detail import DetailView

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
    url(r'^$', cal.views.index, {}, 'cal_index'),
    url(r'^(?P<year>\d{4})/$', YearArchiveView.as_view(
        queryset=Event.all.all(),
        date_field="startDate",
        allow_future=True,
        make_object_list=True
    ), {}, "cal_archive_year"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
     cal.views.monthly,),
    url(r'^special/(?P<typ>\w+)/(?P<name>\w+)/$',
     cal.views.display_special_events),
    url(r'^event/(?P<pk>\d+)/$', DetailView.as_view(
        queryset=Event.all.all(),
        context_object_name='event'
    ), {}, 'cal_event_detail'),
    url(r'^event/(?P<object_id>\d+)/update/$',
     cal.views.update_event, {'new': False}),
    url(r'^(?P<object_id>\d+)/update/$',
     cal.views.update_event, {'new': False}),
    url(r'^event/(?P<object_id>\d+)/delete/', cal.views.delete_event),
    url(r'^(?P<object_id>\d+)/delete/', cal.views.delete_event),
    url(r'^event/(?P<object_id>\d+)/icalendar/', cal.views.event_icalendar, {},
     'cal_event_icalendar'),
    url(r'^export/ical/$', cal.views.complete_ical, {}, 'full_ical'),
    url(r'^event/new/$', cal.views.update_event, {'new': True}),
    url(r'^new/$', cal.views.update_event, {'new': True}),
    url(r'^locations/$', cal.views.SpecialListView.as_view(
                            queryset=Location.objects.all(),
                            events_by="Locations")),
    url(r'^categories/$', cal.views.SpecialListView.as_view(
                            queryset=Category.objects.all(),
                            events_by="Categories")),
    url(r'^ajax/list/(?P<number>\d*)/?$', cal.views.event_list),
]
