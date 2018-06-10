from django.conf.urls import *

import announce.views

urlpatterns = [
    url(r'^$', announce.views.announce),
]
