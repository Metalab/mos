from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class WikiChange(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=300)
    author = models.CharField(max_length=300)
    updated = models.DateTimeField()

    def __str__(self):
        return '%s: %s' % (self.author, self. title)
