from django.db import models


class Change(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=300)
    author = models.CharField(max_length=300)
    updated = models.DateTimeField()

    def __str__(self):
        return '%s: %s' % (self.author, self. title)
