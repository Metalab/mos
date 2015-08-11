from django.conf.urls import *


urlpatterns = patterns('',
    (r'^$', 'announce.views.announce'),
)
