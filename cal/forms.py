from __future__ import absolute_import

from django.forms import ModelForm
import django.forms as forms

from django.forms.fields import SplitDateTimeField
from django.contrib.admin.widgets import AdminSplitDateTime
from .models import Event


class EventForm(ModelForm):
    """
    Form to add an event
    """

    startDate = SplitDateTimeField(widget=AdminSplitDateTime)
    endDate = SplitDateTimeField(required=False, widget=AdminSplitDateTime)
    teaser = forms.CharField(required=False)

    class Meta:
        model = Event
        exclude = ('where', 'created_at', 'created_by', 'deleted', 'who')
