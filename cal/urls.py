from django.conf.urls import *

from django.views.generic.dates import YearArchiveView
from django.views.generic.detail import DetailView

from mos.cal.models import Event, Location, Category
from mos.cal.views import SpecialListView


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


urlpatterns = patterns('',
    (r'^$',
     'mos.cal.views.index', {}, 'cal_index'),
    (r'^(?P<year>\d{4})/$', YearArchiveView.as_view(
        queryset=Event.all.all(),
        date_field="startDate",
        allow_future=True,
        make_object_list=True
    ), {}, "cal_archive_year"),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
     'mos.cal.views.monthly',),
    (r'^special/(?P<typ>\w+)/(?P<name>\w+)/$',
     'mos.cal.views.display_special_events'),
    (r'^event/(?P<pk>\d+)/$', DetailView.as_view(
        queryset=Event.all.all(),
        context_object_name='event'
    ), {}, 'cal_event_detail'),
    (r'^event/(?P<object_id>\d+)/update/$',
     'mos.cal.views.update_event', {'new': False}),
    (r'^(?P<object_id>\d+)/update/$',
     'mos.cal.views.update_event', {'new': False}),
    (r'^event/(?P<object_id>\d+)/delete/', 'mos.cal.views.delete_event'),
    (r'^(?P<object_id>\d+)/delete/', 'mos.cal.views.delete_event'),
    (r'^event/(?P<object_id>\d+)/icalendar/', 'mos.cal.views.event_icalendar', {},
     'cal_event_icalendar'),
    (r'^export/ical/$', 'mos.cal.views.complete_ical', {}, 'full_ical'),
    (r'^event/new/$', 'mos.cal.views.update_event', {'new': True}),
    (r'^new/$', 'mos.cal.views.update_event', {'new': True}),
    (r'^locations/$', SpecialListView.as_view(
                            queryset=Location.objects.all(),
                            events_by="Locations")),
    (r'^categories/$', SpecialListView.as_view(
                            queryset=Category.objects.all(),
                            events_by="Categories")),
    (r'^ajax/list/(?P<number>\d*)/?$', 'mos.cal.views.event_list'),
)
