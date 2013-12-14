from django.conf.urls.defaults import *
from django.views.generic import ListView

from mos.projects.models import Project

info_dict = {
    'queryset': Project.all.all(),
}


urlpatterns = patterns('django.views.generic.dates',
        (r'^$', 
         ListView.as_view(queryset=Project.all.all().order_by('-created_at')[:5],
                          context_object_name="latestprojects",
                          template_name="projects/project_archive.html")),
)

urlpatterns += patterns('',
        (r'^(?P<object_id>\d+)/delete/$',
            'mos.projects.views.delete_project'),
        (r'^(?P<object_id>\d+)/$',
            'django.views.generic.detail.DetailView',
            info_dict),
        (r'^(?P<object_id>\d+)/update/$',
            'mos.projects.views.update_project', {'new': False}),
        (r'^new/$',
            'mos.projects.views.update_project', {'new': True}),
)
