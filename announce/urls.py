from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'mos.announce.views.announce'),
)
