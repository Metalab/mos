import urllib2
import re

from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.conf import settings
from mos.cal.models import Event
from mos.core.context_processors import custom_settings_main
from mos.members.models import get_active_members
from mos.projects.models import Project
from mos.sources.models import WikiChange

def display_main_page(request):
    events = Event.future.get_n(5)
    changes = WikiChange.objects.order_by('-updated')[:5]
    projects = Project.all.order_by('-created_at')[:5]
    randommembers = list(get_active_members().exclude(contactinfo__image="").order_by('?')[:7])

    return render_to_response('index.html', {
        'event_error_id': ' ',
        'latestevents': events,
        'latestchanges': changes,
        'latestprojects': projects,
        'randommembers': randommembers,
    }, context_instance=RequestContext(request, processors=[custom_settings_main]))

def display_cellardoor(request):
    events = Event.future.all()
    return render_to_response('cellardoor.html', {'latestevents': events}, context_instance=RequestContext(request, processors=[custom_settings_main]))
