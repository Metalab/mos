#!/usr/bin/env python
import sys
import os

_DIRNAME = os.path.dirname(globals()["__file__"])
sys.path.append(os.path.join(_DIRNAME, '..'))
sys.path.append('/django/svn/trunk')
from django.core.management import setup_environ
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
    setup_environ(settings)
    from  members.models import *
    members_on_intern = get_mailinglist_members().filter(contactinfo__on_intern_list=True)
    addresses = [x.contactinfo_set.all()[0].intern_list_email for x in members_on_intern if x.contactinfo_set.all()[0].intern_list_email != '']
    sys.stdout.write('\n'.join(addresses))
