from django.http import HttpResponse
from django.utils.html import escape
from django.conf import settings
from mos.usbherelist.models import Usbhereitem
import os
import os.path
import time
import django.template as template
from django.shortcuts import render_to_response


def update_herelist(request):
    r = HttpResponse()
    if request.FILES:
        for k, v in request.FILES.items():
            if v['content-type'] == 'text/plain' and k == 'herelist':
                fd = open(os.path.join(settings.MEDIA_ROOT, 'usbherelist',\
                                       'herelist.txt'), 'wb')
                fd.write(v['content'])
                fd.close()
                r.write('accepted update')
            else:
                r.write('unexpected content-type or name')
    else:
        r.write('no file included')
    return r


def serve_herelist(request, template):
    return render_to_response(template, {'herelist': get_herelist()})


def get_herelist():
    filename = os.path.join(settings.MEDIA_ROOT, 'usbherelist', 'herelist.txt')

    logfile = os.path.join(settings.MEDIA_ROOT, 'test.log')

    herelist = list()

    # a) empty file
    if os.path.getsize(filename) <= 0:
        return None
    # b) too old file: > 45 minutes
    if time.time() - os.path.getmtime(filename) > 60*45:
        return None
    # c) print it
    fd = open(filename, 'rb')
    try:
        for line in fd:
            herelist.append(Usbhereitem(line))
    finally:
        fd.close()

    logfile_fd = open(logfile, 'a')
    logfile_fd.write(herelist.__str__())
    logfile_fd.write('\n')

    logfile_fd.close()

    return herelist
