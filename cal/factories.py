import datetime
import factory
import faker

from .models import Event


class EventFactory(factory.Factory):
    name = faker.company.bs()
    teaser = faker.company.catch_phrase()
    startDate = datetime.date.today()
    endDate = datetime.date.today()

    class Meta:
        model = Event
