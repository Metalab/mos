from __future__ import absolute_import

from django.conf.urls import *
from django.views.generic import ListView, DetailView

from .models import Project
import projects.views


urlpatterns = [
        url(r'^$', ListView.as_view(
            queryset=Project.all.all().order_by('-created_at')[:5],
            context_object_name="latestprojects",
            template_name="projects/project_archive.html")),
        url(r'^(?P<object_id>\d+)/delete/$',
            projects.views.delete_project),
        url(r'^(?P<pk>\d+)/$', DetailView.as_view(
            queryset=Project.all.all()
        )),
        url(r'^(?P<object_id>\d+)/update/$', projects.views.update_project),
        url(r'^new/$', projects.views.update_project),
]
