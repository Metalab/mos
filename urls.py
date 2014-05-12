from django.conf import settings

from django.conf.urls import *
from django.conf.urls.static import static
from django.contrib import admin

from mos.cal.feeds import EventFeed


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
    (r'^admin/', include(admin.site.urls)),

    (r'^feeds/events/$', EventFeed()),

    (r'^calendar/', include('mos.cal.urls')),
    (r'^project/', include('mos.projects.urls')),
    (r'^member/', include('mos.members.urls')),
    (r'^announce/$', include('mos.announce.urls')),
    (r'^cellardoor/', 'mos.web.views.display_cellardoor'),
    (r'^$', 'mos.web.views.display_main_page'),
)

urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
