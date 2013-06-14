from django.conf import settings

from django.conf.urls.defaults import *
from django.contrib import admin

from mos.admin import calendar_admin, project_admin, member_admin, scrooge_admin
from mos.cal.feeds import EventFeed


feeds = {
    'events': EventFeed,
}

admin.autodiscover()

urlpatterns = patterns('',
   (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.Feed', {'feed_dict': feeds}),

    (r'^calendar/', include('mos.cal.urls')),
    (r'^rss/', include('mos.rss.urls')),

    (r'^project/', include('mos.projects.urls')),
    (r'^scrooge/', include('mos.scrooge.urls')),

    (r'^$', 'mos.web.views.display_main_page'),

    (r'^site_media/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    (r'^admin/calendar/', include(calendar_admin.urls)),
    (r'^admin/projects/', include(project_admin.urls)),
    (r'^admin/members/', include(member_admin.urls)),
    (r'^admin/scrooge/', include(scrooge_admin.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^member/', include('mos.members.urls')),

    (r'^wiki/.*$', 'mos.web.views.wikipage'),
#    (r'^usbherelist/', include('mos.usbherelist.urls')),

    (r'^announce/$', include('mos.announce.urls')),

    (r'^cellardoor/', 'mos.web.views.display_cellardoor'),
)
