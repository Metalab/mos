from django.conf.urls.defaults import *
from mos import settings

from mos.projects.models import Project

date_dict = {
    'queryset': Project.all.all(), #finished_at__exact=None),
    'date_field': 'created_at',
    'num_latest': 5,
    'template_object_name': 'latestprojects',
}

info_dict = {
    'queryset': Project.all.all(),
}


urlpatterns = patterns('django.views.generic.date_based',
                       (r'^$', 'archive_index', date_dict),
)

urlpatterns += patterns('',
                        (r'^(?P<object_id>\d+)/delete/$',
                         'mos.projects.views.delete_project'),
                        (r'^(?P<object_id>\d+)/$',
                         'django.views.generic.list_detail.object_detail',
                         info_dict),
                        (r'^(?P<object_id>\d+)/update/$',
                         'mos.projects.views.update_project', {'new': False}),
                        (r'^new/$',
                         'mos.projects.views.update_project', {'new': True}),
)
