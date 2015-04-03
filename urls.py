import settings

from django.conf.urls.defaults import *
from django.contrib import admin

from mos.admin import calendar_admin, project_admin, member_admin, scrooge_admin
from mos.cal.feeds import EventFeed


feeds = {
        'events': EventFeed,
        }

admin.autodiscover()

urlpatterns = patterns('',
   (r'^feeds/(?P<url>.*)/$',
      'django.contrib.syndication.views.feed', {'feed_dict': feeds}),

    (r'^calendar/', include('mos.cal.urls')),
    (r'^rss/', include('mos.rss.urls')),

    (r'^project/', include('mos.projects.urls')),
    (r'^scrooge/', include('mos.scrooge.urls')),

    (r'^$', 'mos.web.views.display_main_page'),

    (r'^site_media/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    (r'^admin/calendar/(.*)', calendar_admin.root),
    (r'^admin/projects/(.*)', project_admin.root),
    (r'^admin/members/(.*)', member_admin.root),
    (r'^admin/scrooge/(.*)', scrooge_admin.root),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),

    (r'^member/', include('mos.members.urls')),

    (r'^wiki/.*$', 'mos.web.views.wikipage'),
#    (r'^usbherelist/', include('mos.usbherelist.urls')),

    (r'^announce/$', include('mos.announce.urls')),

    (r'^cellardoor/', 'mos.web.views.display_cellardoor'),
    (r'^spaceapi.json$', 'mos.web.views.spaceapi'),
)
