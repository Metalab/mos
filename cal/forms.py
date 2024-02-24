from django.forms import ModelForm
import django.forms as forms

from django.forms.fields import SplitDateTimeField
from django.contrib.admin.widgets import AdminSplitDateTime
from .models import Event
import re
import requests


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
        wikipage = re.sub(r'^http(s)://metalab.at/wiki/', '',cleaned_data.get('wikiPage'))
        cleaned_data['wikiPage'] = wikipage
        if cleaned_data.get('advertise') and re.match(r'^(Benutzer|User):', wikipage):
            self.add_error('wikiPage', 'Userpages don\'t provide adequate information for public Events')

        r = requests.get('https://metalab.at/wiki/%s' % wikipage)
        
        if r.status_code == 404:
            self.add_error('wikiPage', 'Wikipage not found: https://metalab.at/wiki/%s' % wikipage) #TODO Figure out how to make clickable
        return cleaned_data