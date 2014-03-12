from django.conf.urls import *
from django.views.generic import ListView, DetailView

from mos.projects.models import Project


urlpatterns = patterns('',
        (r'^$', ListView.as_view(
            queryset=Project.all.all().order_by('-created_at')[:5],
            context_object_name="latestprojects",
            template_name="projects/project_archive.html")),
        (r'^(?P<object_id>\d+)/delete/$',
            'mos.projects.views.delete_project'),
        (r'^(?P<pk>\d+)/$', DetailView.as_view(
            queryset=Project.all.all()
        )),
        (r'^(?P<object_id>\d+)/update/$',
            'mos.projects.views.update_project', {'new': False}),
        (r'^new/$',
            'mos.projects.views.update_project', {'new': True}),
)
