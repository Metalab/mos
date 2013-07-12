from django.conf import settings

from django.conf.urls.defaults import *
from django.contrib import admin

from mos.cal.feeds import EventFeed


feeds = {
    'events': EventFeed,
}

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.Feed', {'feed_dict': feeds}),

    (r'^calendar/', include('mos.cal.urls')),
    (r'^rss/', include('mos.rss.urls')),

    (r'^project/', include('mos.projects.urls')),
    (r'^scrooge/', include('mos.scrooge.urls')),

    (r'^$', 'mos.web.views.display_main_page'),

    (r'^member/', include('mos.members.urls')),

    (r'^wiki/.*$', 'mos.web.views.wikipage'),
#    (r'^usbherelist/', include('mos.usbherelist.urls')),

    (r'^announce/$', include('mos.announce.urls')),

    (r'^cellardoor/', 'mos.web.views.display_cellardoor'),
)
