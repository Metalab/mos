from django.db import models
from django.contrib.auth.models import User
import string
import random


def random_pwd():
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(32))

class Device(models.Model):
    name_validator = RegexValidator(r'^[-_0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    name = models.CharField(max_length=255, unique=True, validators=[name_validator])
    authkey = models.CharField(max_length=255, default=random_pwd)
    expose_usernames = models.BooleanField(default=False)

    def __str__(self):
        return u"%s" % (self.name)

class UserPermission(models.Model):
    user = models.OneToOneField(User)
    key_id = models.CharField(max_length=100)
    device = models.ManyToManyField(Device, blank=False)
    last_used = models.DateField(auto_now_add=True)

    def __str__(self):
        return u"%s" % (self.user.username)
