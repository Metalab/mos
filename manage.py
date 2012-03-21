#!/usr/bin/env python
import sys
import os

_DIRNAME = os.path.dirname(globals()["__file__"])
sys.path.append(os.path.join(_DIRNAME, '..'))
sys.path.append('/django/svn/trunk')
from django.core.management import execute_manager
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the \
                      directory containing %r. It appears you've \
                      customized things.\nYou'll have to run django-admin.py,\
                      passing it your settings module.\n(If the file \
                      settings.py does indeed exist, it's causing an \
                      ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
