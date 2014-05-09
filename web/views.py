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
from mos.rss.models import Change

def display_main_page(request):
    events = Event.future.get_n(5)
    changes = Change.objects.order_by('-updated')[:5]
    projects = Project.all.order_by('-created_at')[:5]
    randommembers = list(get_active_members().exclude(contactinfo__image="").order_by('?')[:7])

    return render_to_response('index.html', {
        'event_error_id': ' ',
        'latestevents': events,
        'latestchanges': changes,
        'latestprojects': projects,
        'randommembers': randommembers,
    }, context_instance=RequestContext(request, processors=[custom_settings_main]))


def wikipage(request):

    path = request.path[10:-1]
    url = "%s/%s" % (settings.HOS_WIKI_URL, path)
    page = urllib2.urlopen(url).read()

    start = page.find('<!-- start content -->')
    end = page.find('<!-- end content -->')
    page = page[start:end]

    page = re.compile('href="\/wiki').sub("href=\"%s" % settings.HOS_WIKI_URL, page)
    page = re.compile('src="\/wiki').sub("src=\"%s" % settings.HOS_WIKI_URL, page)

    return render_to_response('wikipage.html', {
        'file': page,
    }, context_instance=RequestContext(request))


def display_cellardoor(request):
    events = Event.future.all()
    return render_to_response('cellardoor.html', {'latestevents': events}, context_instance=RequestContext(request, processors=[custom_settings_main]))
