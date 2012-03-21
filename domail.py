import os
import sys

from mos.members.models import get_active_members


os.environ['DJANGO_SETTINGS_MODULE'] = "mos.settings"
sys.path.append("/django/deployment")


for user in get_active_members():
    user.is_active = True
    user.save()

    print user, user.email
