from django.conf import settings


def custom_settings_global(request):
    """
    sets custom style and name as global template variables
    """

    return {'custom_style': settings.HOS_CUSTOM_STYLE,
            'HOS_NAME': settings.HOS_NAME,
            }


def custom_settings_wiki(request):
    """
    Sets the custom wiki url
    """

    return {'HOS_WIKI_URL': settings.HOS_WIKI_URL}


def custom_settings_main(request):
    """
    sets customizations specified in settings.py for the main page
    """

    return {'introduction_text': settings.HOS_INTRODUCTION,
            'members': settings.HOS_MEMBER_GALLERY,
            'gallery': settings.HOS_LOCATION_GALLERY,
            'openlab': settings.HOS_OPENLAB,
            'calendar': settings.HOS_CALENDAR,
            'projects': settings.HOS_PROJECTS,
            'recent_changes': settings.HOS_RECENT_CHANGES,
            'metasense': settings.HOS_METASENSE,
            'HOS_WIKI_CHANGE_URL': settings.HOS_WIKI_CHANGE_URL,
            }
