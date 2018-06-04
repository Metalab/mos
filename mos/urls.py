from django.conf import settings

from django.conf.urls import *
from django.conf.urls.static import static
from django.contrib import admin
import django.views.i18n

from cal.feeds import EventFeed
import web.views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/jsi18n/', django.views.i18n.javascript_catalog),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^feeds/events/$', EventFeed()),

    url(r'^calendar/', include('cal.urls')),
    url(r'^project/', include('projects.urls')),
    url(r'^member/', include('members.urls')),
    url(r'^announce/', include('announce.urls')),
    url(r'^cellardoor/', web.views.display_cellardoor),
    url(r'^spaceapi.json$', web.views.spaceapi),
    url(r'^$', web.views.display_main_page),
]

urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
