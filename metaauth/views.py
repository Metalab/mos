from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
import base64
from .models import Device, UserPermission
from django.core.exceptions import ObjectDoesNotExist
from django.template import TemplateDoesNotExist

def keys(request):

    # https://djangosnippets.org/snippets/1304/
    # Check for valid basic auth header
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            if auth[0].lower() == "basic":
                uname, passwd = base64.b64decode(auth[1]).split(':')
                try:
                    device = Device.objects.get(name=uname, authkey=passwd)
                except ObjectDoesNotExist:
                    return HttpResponse('Unauthorized', status=401)

                # use custom template for device if it exists
                try:
                    template = get_template('device_%s.csv' % uname)
                except TemplateDoesNotExist:
                    if device.expose_usernames:
                        template = get_template('with_usernames.csv')
                    else:
                        template = get_template('without_usernames.csv')

                context = {
                    'user_permission': UserPermission.objects.filter(device=device),
                }
                content = template.render(context)
                return HttpResponse(content, content_type='text/csv', status=200)
    return HttpResponse('Unauthorized', status=401)
