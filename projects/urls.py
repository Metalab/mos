from __future__ import absolute_import

from django.urls import path, re_path
from django.views.generic import ListView, DetailView

from .models import Project
import projects.views


urlpatterns = [
    path('',
        ListView.as_view(
            queryset=Project.all.all().order_by('-created_at')[:5],
            context_object_name="latestprojects",
            template_name="projects/project_archive.html",
        ),
    ),
    re_path(
        r'^(?P<object_id>\d+)/delete/$',
        projects.views.delete_project,
    ),
    re_path(
        r'^(?P<pk>\d+)/$',
        DetailView.as_view(
            queryset=Project.all.all()
        ),
    ),
    re_path(
        r'^(?P<object_id>\d+)/update/$',
        projects.views.update_project,
    ),
    path(
        'new/',
        projects.views.update_project,
    ),
]
