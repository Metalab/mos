import datetime
import time
import feedparser
from contextlib import contextmanager

from django.test import TestCase
from django.core.management.base import CommandError
from django.conf import settings

from .models import WikiChange
from .management.commands import get_wiki_changes


class FakeFeed:
    class FakeFeedEntry:
        link = ''
        author = ''
        updated_parsed = time.strptime('2000-01-01', '%Y-%m-%d')

        def __init__(self, title):
            self.title = title

    def __init__(self, url):
        pass

    def __contains__(self, key):
        return False

    def __getattr__(self, attr):
        return [self.FakeFeedEntry(c) for c in 'qwert']


class CronJobTest(TestCase):
    def setUp(self):
        self.cmd = get_wiki_changes.Command()

        dt = datetime.datetime.now()
        self.changes = [WikiChange(title=t, updated=dt) for t in 'asdfg']
        WikiChange.objects.bulk_create(self.changes)

    def test_raises_exception_on_parse_error(self):
        real_url = settings.MOS_WIKI_CHANGE_URL
        settings.MOS_WIKI_CHANGE_URL = 'xxx'

        self.assertRaises(CommandError, self.cmd.handle_noargs)

        settings.MOS_WIKI_CHANGE_URL = real_url

    def test_no_db_changes_on_error(self):
        real_url = settings.MOS_WIKI_CHANGE_URL
        settings.MOS_WIKI_CHANGE_URL = 'xxx'

        try:
            self.cmd.handle_noargs()
        except:
            pass

        self.assertEqual(WikiChange.objects.count(), 5)
        for c in 'asdfg':
            WikiChange.objects.get(title=c) # does not raise

        settings.MOS_WIKI_CHANGE_URL = real_url

    def test_old_entries_are_deleted(self):
        self.cmd.handle_noargs()
        for c in 'asdfg':
            self.assertRaises(WikiChange.DoesNotExist,
                              WikiChange.objects.get, title=c)

    def test_five_entries_are_kept(self):
        real_parse = feedparser.parse

        try:
            feedparser.parse = FakeFeed
            self.cmd.handle_noargs()
            self.assertEqual(WikiChange.objects.count(), 5)

            for c in 'qwert':
                WikiChange.objects.get(title=c) # does not raise
            for c in 'asdfg':
                self.assertRaises(
                    WikiChange.DoesNotExist,
                    WikiChange.objects.get, title=c
                )
        finally:
            feedparser.parse = real_parse
