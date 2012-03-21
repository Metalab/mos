from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from mos.cal.forms import EventForm
from mos.cal.models import Event


correct_data = {'name': 'TestEvent1',
                'teaser': 'Event des Jahres',
                'wikiPage': '/wiki/foo',
                'startDate_0': '2008-06-06',
                'startDate_1': '15:00',
                'endDate_0': '2009-04-02',
                'endDate_1': '14:00'}


class EventFormTest(TestCase):
    fixtures = ['initial_user.json']

    def setUp(self):
        self.wrong_data = correct_data.copy()

       #set error conditions
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
        print f.errors

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

        response = self.c.post('/cal/new/',  # adds a new event via
                               correct_data) # the view update_event
        self.assertContains(response, 'TestEvent1', count=None,
                            status_code=200)
        self.assertContains(response, '06.06.2008 15:00', count=None,
                            status_code=200)

        response = self.c.post('/cal/new/',           # adds a new  event via
                               self.minimal_data_set) # the view update_event
        self.assertContains(response, 'TestEvent1', count=None,
                            status_code=200)
        self.assertContains(response, '06.06.2008 15:00', count=None,
                            status_code=200)
