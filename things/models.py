from django.contrib.auth.models import User
from django.db import models
from django.utils.crypto import get_random_string


def make_token():
    return get_random_string(42)


class Thing(models.Model):
    """ Something in the hackspace that people can get permission to use, e.g. the laser or the door """
    slug = models.SlugField(unique=True, help_text="Name of the thing, e.g. 'laser'")
    token = models.CharField(max_length=128, default=make_token, help_text="auto generated, allows the machine to get the key IDs, KEEP SECRET")

    def __str__(self):
        return "Thing " + self.slug


class ThingUser(models.Model):
    """ Allows a user to use a thing, e.g. user ripper has permission to use the laser """
    thing = models.ForeignKey(Thing, on_delete=models.PROTECT)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="thingusers",
    )
    created_at = models.DateField(auto_now_add=True)
    best_before = models.DateField(
        help_text="Wann die Schulung wiederholt werden sollte",
        null=True,
        blank=True,
    )


class ThingEvent(models.Model):
    class Kind(models.TextChoices):
        LOGIN = ("LOGIN", "Login")
        LOGOUT = ("LOGOUT", "Logout")
        USAGE_MEMBER = ("USAGE_MEMBER", "Zeit (Member)")
        USAGE_NONMEMBER = ("USAGE_NONMEMBER", "Zeit (Nicht-Member)")
        USAGE_METALAB = ("USAGE_METALAB", "Zeit (für Metalab)")

    thing = models.ForeignKey(Thing, on_delete=models.PROTECT)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="thingevents",
    )
    kind = models.CharField(
        max_length=32,
        db_index=True,
        choices=Kind.choices,
    )
    usage_seconds = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
