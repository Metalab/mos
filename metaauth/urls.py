from django.conf.urls import *

# place app url patterns here
urlpatterns = patterns('',
    (r'^keys$', 'metaauth.views.keys'),
)

