from django.db import models


class Category(models.Model):
    """
    represents a Category (name, description)
    used in cal.models.Event
    """

    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)

    def __str__(self):
        return u"%s" % self.name


class Location(models.Model):
    """
    represents a location(name, description, country)
    used in cal.models.Event
    """

    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)

    country = models.CharField(max_length=100)

    def __str__(self):
        return u"%s" % self.name
