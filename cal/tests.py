from datetime import datetime, timedelta
import unittest

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import Client

from .forms import EventForm
from .models import Event
from .feeds import EventFeed


correct_data = {'name': 'TestEvent1',
                'teaser': 'Event des Jahres',
                'wikiPage': '/wiki/foo',
                'startDate_0': '2008-06-06',
                'startDate_1': '15:00',
                'endDate_0': '2009-04-02',
                'endDate_1': '14:00'}


class EventTest(TestCase):
    fixtures = ['initial_user.json']

    @unittest.skip("not implemented")
    def testBackwardsDateRange(self):
        """Creates an event that ends before it starts"""
        e = Event(
            name="Clever event name",
            wikiPage="/wiki/foo",
            startDate=datetime(2024, 2, 24, 16, 15, 0),
            endDate=datetime(2024, 2, 23, 16, 15, 0),
            created_by=User.objects.first(),
        )
        with self.assertRaises(
            ValidationError,
            msg="Event has to have non-zero duration"
        ):
            e.save()

    @unittest.skip("not implemented")
    def testZeroDateRange(self):
        """Creates an event that ends immediately"""
        e = Event(
            name="Clever event name",
            wikiPage="/wiki/foo",
            startDate=datetime(2024, 2, 24, 16, 15, 0),
            endDate=datetime(2024, 2, 24, 16, 15, 0),
            created_by=User.objects.first(),
        )
        with self.assertRaises(ValidationError, msg="Event has to ha"):
            e.save()


class EventFormTest(TestCase):
    fixtures = ['initial_user.json']

    def setUp(self):
        self.wrong_data = correct_data.copy()

        # set error conditions
        self.wrong_data['name'] = ''
        self.wrong_data['startDate_0'] = 'asdasd'
        self.wrong_data['endDate_1'] = 'foop'
        self.wrong_data['wikiPage'] = ''

    def testFormCorrectData(self):
        """Creates a event form with valid information"""

        f = EventForm(correct_data)
        assert f.is_valid() is True, 'Correct set of event data but form\
                                      errors'

    def testFormWrongData(self):
        """Creates a event form with invalid information"""

        f = EventForm(self.wrong_data)
        assert f.is_valid() is False, 'Name of the event is missing, but no\
                                       error raised'
        assert f.errors['name'] != "", 'Name of the event is missing, but no \
                                        error raised'
        assert f.errors['startDate'] != "", 'Wrong date, but no error raised'
        assert f.errors['endDate'] != "", 'Wrong time, but no error raised'
        assert f.errors['wikiPage'] != "", 'Wikipage missing, but no error \
                                            raised'

    def testBackwardsDateRange(self):
        """Submits an event that ends before it starts"""

        data = correct_data.copy()
        start, end = data['startDate_0'], data['endDate_0']
        data['startDate_0'], data['endDate_0'] = end, start

        f = EventForm(data)
        assert f.has_error('endDate'), "Event can end before it starts"

    def testZeroDateRange(self):
        """Submits an event that ends immediately."""
        data = correct_data.copy()
        data['endDate_0'] = data['startDate_0']
        data['endDate_1'] = data['startDate_1']

        f = EventForm(data)
        assert f.is_valid(), "Event has to have a non-zero duration"

    def testSaveFromForm(self):
        """Adds  a user with valid information"""

        f = EventForm(correct_data)
        if f.is_valid():
            event_data = f.save(commit=False)
            user = User.objects.get(username='d3f3nd3r')
            event_data.save(editor=user, new=True)

        assert Event.objects.get(name='TestEvent1'), 'couldnt add event'


class EventViewsTest(TestCase):
    fixtures = ['initial_user.json']

    def setUp(self):
        self.c = Client()
        self.c.login(username='d3f3nd3r', password='d3f3nd3r')

        self.minimal_data_set = correct_data.copy()
        self.minimal_data_set['endDate_0'] = ''
        self.minimal_data_set['endDate_1'] = ''
        self.minimal_data_set['teaser'] = ''

    def testAddNewEvent(self):
        """ Adds a new event via the view """

        response = self.c.post('/calendar/new/',   # adds a new event via
                               correct_data)  # the view update_event
        self.assertContains(response, 'TestEvent1', count=None,
                            status_code=200)
        self.assertContains(response, '06.06.2008 15:00', count=None,
                            status_code=200)

        response = self.c.post('/calendar/new/',            # adds a new  event via
                               self.minimal_data_set)  # the view update_event
        self.assertContains(response, 'TestEvent1', count=None,
                            status_code=200)
        self.assertContains(response, '06.06.2008 15:00', count=None,
                            status_code=200)


class EventFeedTest(TestCase):
    def setUp(self):
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        tommorrow = now + timedelta(days=1)

        defaults = {'username': 'admin'}
        user, _ = User.objects.get_or_create(pk=1, defaults=defaults)

        self.past_event = Event()
        self.past_event.startDate = yesterday
        self.past_event.endDate = yesterday
        self.past_event.created_by_id = 1
        self.past_event.save()
        self.future_event = Event()
        self.future_event.startDate = tommorrow
        self.future_event.endDate = tommorrow
        self.future_event.created_by_id = 1
        self.future_event.save()
        self.running_event = Event()
        self.running_event.startDate = yesterday
        self.running_event.endDate = tommorrow
        self.running_event.created_by_id = 1
        self.running_event.save()

        self.items = EventFeed().items()

    def testRunningEvents(self):
        self.assertIn(self.running_event, self.items)

    def testFutureEvents(self):
        self.assertIn(self.future_event, self.items)

    def testPastEvents(self):
        self.assertNotIn(self.past_event, self.items)
