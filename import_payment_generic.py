#!/usr/bin/env python3
import os,sys


_DIRNAME = os.path.dirname(globals()["__file__"])
sys.path.append(os.path.join(_DIRNAME, '..'))
sys.path.append('/django/svn/trunk')
from django.core.management import setup_environ
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the \
                      directory containing %r. It appears you've \
                      customized things.\nYou'll have to run django-admin.py,\
                      passing it your settings module.\n(If the file \
                      settings.py does indeed exist, it's causing an \
                      ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    setup_environ(settings)
    from  members.models import *
    if len(sys.argv) < 2:
        print("%s <filename>" % sys.argv[0])
        sys.exit(1)

    Payment.objects.import_generic(sys.argv[1])
