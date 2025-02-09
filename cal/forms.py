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

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('startDate')
        end_date = cleaned_data.get('endDate')
        if end_date and end_date < start_date:
            self.add_error('endDate', 'End date must be greater than start date')
        
        loc = cleaned_data.get('location').name
        if loc not in ('any rooom', 'online', 'Woanders'): #
            if Event.objects.exclude(id=self.instance.id).filter(location__name=loc, startDate__lte=end_date, endDate__gte=start_date).count() != 0 or \
               Event.objects.exclude(id=self.instance.id).filter(location__name='all rooms', startDate__lte=end_date, endDate__gte=start_date).count() != 0:
                self.add_error('location', 'This location is already in use during the selected time')
        if loc == 'all rooms' and Event.objects.exclude(id=self.instance.id).exclude(location__name__in=('any rooom', 'online', 'Woanders')) \
                .filter(startDate__lte=end_date, endDate__gte=start_date).count() != 0:
            self.add_error('location', 'This location is already in use during the selected time')      
        
        category = cleaned_data.get('category')

        if cleaned_data.get('wikiPage'):
            wikipage, _ = re.subn(r'(^http(s)://metalab.at/wiki/|\.\.|\ |\%|\&)', '', cleaned_data.get('wikiPage'), 200)
            cleaned_data['wikiPage'] = wikipage
            if cleaned_data.get('advertise') and re.match(r'^(Benutzer(in)?|User):', wikipage):
                self.add_error('wikiPage', 'Userpages don\'t provide adequate information for public Events')

            r = requests.get('https://metalab.at/wiki/%s' % wikipage)

            if r.status_code == 404 and (not category or category.name != "jour fixe"):
                self.add_error('wikiPage', 'Wikipage not found: https://metalab.at/wiki/%s' % wikipage) #TODO Figure out how to make clickable
        return cleaned_data
