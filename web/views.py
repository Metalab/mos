from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

from cal.models import Event
from core.context_processors import custom_settings_main
from members.models import get_active_members
from projects.models import Project
from sources.models import WikiChange



def display_main_page(request):
    events = Event.future.get_n(5)
    changes = WikiChange.objects.order_by('-updated')[:5]
    projects = Project.all.order_by('-created_at')[:5]
    randommembers = list(get_active_members().exclude(contactinfo__image="").order_by('?')[:7])

    context = custom_settings_main(request)
    context.update(
        {'event_error_id': ' ',
        'latestevents': events,
        'more_events_url': 'calendar/',
        'latestchanges': changes,
        'latestprojects': projects,
        'randommembers': randommembers}
    )
    return render(request, 'index.html', context)


def display_cellardoor(request):
    context = custom_settings_main(request)
    context['latestevents'] = Event.future.all()
    return render(request, 'cellardoor.html', context)


def spaceapi(request):
    # See http://spaceapi.net/documentation

    projects = Project.all.order_by('-created_at')[:5]

    return JsonResponse({
        'api': '0.13',
        'space': 'Metalab',
        'logo': 'https://metalab.at/static/images/logo.png',
        'url': 'https://metalab.at/',
        'location': {
            # https://metalab.at/wiki/Lage
            'address': u'Rathausstra\xdfe 6, 1010 Vienna, Austria',
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
                'url': settings.MOS_WIKI_CHANGE_URL,
            },
            'calendar': {
                'type': 'rss',
                'url': 'https://metalab.at/feeds/events/',
            },
            'blog': {
                'type': 'rss',
                'url': 'http://metalab.soup.io/rss',
            },
        },
        'projects': ['https://metalab.at/wiki/%s' % project.wikiPage for project in projects if project.wikiPage],
        'state': {
            # TODO: Implement open state tracking
            'open': None,
        },
    })
