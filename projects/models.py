from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db import models


class ProjectManager(models.Manager):

    def get_queryset(self):
        return super(ProjectManager, self).get_queryset().filter(deleted=False)


@python_2_unicode_compatible
class Project(models.Model):
    name = models.CharField(max_length=200)
    teaser = models.TextField(max_length=200, blank=True, null=True)
    wikiPage = models.CharField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(default=datetime.datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    finished_at = models.DateField(blank=True, null=True)
    deleted = models.BooleanField(default=False)

    objects = models.Manager()
    all = ProjectManager()

    def __str__(self):
        return self.name

    def delete(self):
        self.deleted = True
        self.save()
