from django.conf import settings

from django.conf.urls import *
from django.conf.urls.static import static
from django.contrib import admin

from cal.feeds import EventFeed


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
    (r'^admin/', include(admin.site.urls)),

    (r'^feeds/events/$', EventFeed()),

    (r'^calendar/', include('cal.urls')),
    (r'^project/', include('projects.urls')),
    (r'^member/', include('members.urls')),
    (r'^announce/$', include('announce.urls')),
    (r'^cellardoor/', 'web.views.display_cellardoor'),
    (r'^spaceapi.json$', 'web.views.spaceapi'),
    (r'^$', 'web.views.display_main_page'),
)

urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
