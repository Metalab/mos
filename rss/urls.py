from django.conf.urls import *
from django.views.generic import ArchiveIndexView

from models import Change


urlpatterns = patterns('',
#(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
# 'object_detail', date_dict),
#(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',
#'archive_day',   date_dict),
#(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
#'archive_month', date_dict),
#(r'^(?P<year>\d{4})/$', archive_year',  date_dict),
    (r'^$', ArchiveIndexView.as_view(
        queryset = Change.objects.all(),
        date_field = 'updated',
        allow_future = True,
        allow_empty = True,
        context_object_name='latestchanges',
    )),
)
