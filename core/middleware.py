"""
django_playground.core.middleware
inspired by www.pylucid.org
see http://trac.pylucid.net/browser/trunk/pylucid/PyLucid/middlewares/\
pagestats.py for authors
"""
import time

from django.db import connection
from django.utils.encoding import force_unicode
from mos.core.utils import human_readable_time


TAG = '<!-- footer_stats -->'
FOOTER_STAT_STRING = 'renderd in %(render_time)s - %(queries)s sql queries'


class SetStatFooter:
    """
    Sets some performance data (number of queries,..
    """

    def process_request(self, request):
        self.time_started = time.time()
        self.old_queries = len(connection.queries)

    def process_response(self, request, response):
        try:
            if 'text/html' not in response['Content-Type']:
                return response
            if request.is_ajax():
                return response
            if response.status_code != 200:
                return response

            queries = len(connection.queries) - self.old_queries

            render_time = human_readable_time(time.time() - self.time_started)
            stats = FOOTER_STAT_STRING % {'render_time': render_time,
                                          'queries': queries}
            content = response.content
            response.content = force_unicode(content).replace(TAG, stats)
        except:
            pass

        return response
