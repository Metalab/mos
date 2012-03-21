from django.db import models


class Usbhereitem:

    def __init__(self, nick=""):
        self.nick = nick

    def __str__(self):
        return "%s" % (self.nick)

    def __unicode__(self):
        return "%s" % (self.nick)
