import os
import random
import urllib2
import re
from stat import *

from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext

from mos import settings
from mos.cal.models import Event
from mos.core.context_processors import custom_settings_main
from mos.members.models import get_active_members
from mos.projects.models import Project
from mos.rss.models import Change
from mos.usbherelist.views import get_herelist


def gallery_images(top):
    imgs = []
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname)[ST_MODE]
        if S_ISREG(mode):
            path = "site_media/gallerypics/%s" % os.path.basename(pathname)
            if pathname.find(".jpg") != -1:
                imgs.append(path)
    return imgs


def flickr_link(name):
    name = name.split('_')[0]
    return "http://flickr.com/photo_zoom.gne?id="+name+"&size=m"


def flickr_images(image_urls):
    images = []
    for image_url in image_urls:
        images_dict = dict()
        images_dict['src'] = image_url
        images_dict['href'] = flickr_link(os.path.basename(image_url))
        images.append(images_dict)
    return images


def display_main_page(request):
    events = Event.future.get_n(5)
    changes = Change.objects.order_by('-updated')[:5]
    projects = Project.all.order_by('-created_at')[:5]
    randommembers = list(get_active_members().exclude(contactinfo__image="")\
                                                            .order_by('?')[:7])
    herelist = get_herelist()

    path = os.path.join(settings._DIRNAME, "media/gallerypics/")
    image_urls = gallery_images(path)
    random.shuffle(image_urls)
    image_urls = image_urls[:2]
    images = flickr_images(image_urls)

    return render_to_response('index.html', {
        'event_error_id': ' ',
        'latestevents': events,
        'latestchanges': changes,
        'latestprojects': projects,
        'images': images,
        'randommembers': randommembers,
        }, context_instance=RequestContext(request,
                                           processors=[custom_settings_main]))


def wikipage(request):

    path = request.path[10:-1]
    url = "%s/%s" % (settings.HOS_WIKI_URL, path)
    page = urllib2.urlopen(url).read()

    start = page.find('<!-- start content -->')
    end = page.find('<!-- end content -->')
    page = page[start:end]

    page = re.compile('href="\/wiki').sub("href=\"%s" % settings.HOS_WIKI_URL,\
                                                                          page)
    page = re.compile('src="\/wiki').sub("src=\"%s" % settings.HOS_WIKI_URL, \
                                                                          page)

    return render_to_response('wikipage.html', {
        'file': page,
        }, context_instance=RequestContext(request))


def display_cellardoor(request):
    events = Event.future.all()
    return render_to_response('cellardoor.html', {'latestevents': events,}, context_instance=RequestContext(request,processors=[custom_settings_main]))


def spaceapi(request):
    # See http://spaceapi.net/documentation

    projects = Project.all.order_by('-created_at')[:5]

    return json_response({
        'api': '0.13',
        'space': 'Metalab',
        'logo': 'https://metalab.at/site_media/images/logo.png',
        'url': 'https://metalab.at/',
        'location': {
            # https://metalab.at/wiki/Lage
            'address': 'Rathausstraße 6, 1010 Vienna, Austria',
            'lat': 48.2093723,
            'lon': 16.356099,
        },
        'contact': {
            'twitter': '@metalab_events',
            'irc': 'irc://irc.freenode.net/#metalab',
            'email': 'core@metalab.at',
            'ml': 'metalab@lists.metalab.at',
            'jabber': 'metalab@conference.jabber.metalab.at',
            'phone': '+43 720 00 23 23',
        },
        'issue_report_channels': [
            'email',
        ],
        'feeds': {
            'wiki': {
                'type': 'atom',
                'url': settings.HOS_WIKI_CHANGE_URL,
            },
            'calendar': {
                'type': 'rss',
                'url': 'https://metalab.at/feeds/events/',
            },
        },
        'projects': ['https://metalab.at/wiki/%s' % project.wikiPage for project in projects if project.wikiPage],
        'state': {
            # TODO: Implement open state tracking
            'open': None,
        },
    })
