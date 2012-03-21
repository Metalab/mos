from django.conf.urls.defaults import *
from mos import settings

urlpatterns = patterns('',
    (r'^$', 'mos.announce.views.announce'),
)
