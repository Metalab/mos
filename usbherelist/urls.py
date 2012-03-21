from django.conf.urls.defaults import *
from mos.usbherelist.views import get_herelist, serve_herelist

info_dict ={
        'template': 'usbherelist/usbherelist.html',
        }

urlpatterns = patterns('',
    (r'update', 'mos.usbherelist.views.update_herelist'),
#    (r'^$', 'django.views.generic.simple.direct_to_template', info_dict),
    (r'^$', serve_herelist, info_dict),
)
