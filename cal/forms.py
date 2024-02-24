from django.forms import ModelForm
import django.forms as forms

from django.forms.fields import SplitDateTimeField
from django.contrib.admin.widgets import AdminSplitDateTime
from .models import Event
import re  


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

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('startDate')
        end_date = cleaned_data.get('endDate')
        if end_date and end_date < start_date:
            self.add_error('endDate', 'End date must be greater than start date')
        cleaned_data['wikiPage'] = re.sub(r'^http(s)://metalab.at/wiki/', '',cleaned_data.get('wikiPage'))
        return cleaned_data
