import datetime
import factory
import faker
from models import Event

class EventFactory(factory.Factory):
    FACTORY_FOR = Event

    name = faker.company.bs()
    teaser = faker.company.catch_phrase()
    startDate = datetime.date.today
    endDate = datetime.date.today
    