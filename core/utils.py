"""
used from pylucid (www.pylucid.org)
see http://trac.pylucid.net/browser/trunk/pylucid/PyLucid/template_addons/\
filters.py for author
information
"""

import time


def human_readable_time(t):
    """ converts (milli-)seconds into a nice string """

    if t<1:
        return ("%.1f ms") % (t * 1000)
    elif t>60:
        return ("%.1f min") % (t/60.0)
    else:
        return ("%.1f sec") % t
