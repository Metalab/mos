from django.conf.urls.defaults import *
from mos import settings

from models import Change
import datetime

date_dict = {
    'queryset': Change.objects.all(),
    'date_field': 'updated',
    'allow_future': True,
    'allow_empty': True,
    'num_latest': 5,
    'template_object_name': 'latestchanges',
}

urlpatterns = patterns('django.views.generic.date_based',
#(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
# 'object_detail', date_dict),
#(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',
#'archive_day',   date_dict),
#(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
#'archive_month', date_dict),
#(r'^(?P<year>\d{4})/$', archive_year',  date_dict),
    (r'^$', 'archive_index', date_dict),
)
