from django.conf.urls import *

urlpatterns = patterns('',
    (r'^$', 'mos.announce.views.announce'),
)
