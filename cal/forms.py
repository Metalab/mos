from django.forms import ModelForm
import django.forms as forms

from mos.cal.fields import DateTimeCombiField
from mos.cal.models import Event


class EventForm(ModelForm):
    """
    Form to add an event
    """

    startDate = DateTimeCombiField()
    endDate = DateTimeCombiField(required=False)
    teaser = forms.CharField(required=False)

    class Meta:
        model = Event
        exclude = ('where', 'created_at', 'created_by', 'deleted', 'who')
