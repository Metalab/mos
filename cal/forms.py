import re

import django.forms as forms
import requests
from django.contrib.admin.widgets import AdminSplitDateTime
from django.forms import ModelForm
from django.forms.fields import SplitDateTimeField

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

    def clean_wiki_url_fields(self, cleaned_data, field):
        if cleaned_data.get(field):
            category = cleaned_data.get('category')
            wikipage, _ = re.subn(r'(^http(s)://metalab.at/wiki/|\.\.|\ |\%|\&)', '', cleaned_data.get(field), 200)
            cleaned_data[field] = wikipage
            if cleaned_data.get('advertise') and re.match(r'^(Benutzer(in)?|User):', wikipage):
                self.add_error(field, 'Userpages don\'t provide adequate information for public Events')

            r = requests.get('https://metalab.at/wiki/%s' % wikipage)

            if r.status_code == 404 and (not category or category.name != "jour fixe"):
                self.add_error(field, 'Wikipage not found: https://metalab.at/wiki/%s' % wikipage) #TODO Figure out how to make clickable

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('startDate')
        end_date = cleaned_data.get('endDate')
        if end_date and end_date < start_date:
            self.add_error('endDate', 'End date must be greater than start date')

        loc = cleaned_data.get('location')
        if loc and loc.name not in ('any rooom', 'online', 'Woanders'): #
            if Event.objects.exclude(id=self.instance.id).filter(deleted=False, location__name=loc.name, startDate__lt=end_date, endDate__gt=start_date).count() != 0:
                self.add_error('location', 'This location is already in use during the selected time')

        self.clean_wiki_url_fields(cleaned_data, "wikiPage")
        self.clean_wiki_url_fields(cleaned_data, "wikiImagePage")

        return cleaned_data
