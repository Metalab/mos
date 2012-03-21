from icalendar import Calendar

def create_calendar(components):
    c = Calendar()
    c.add('version', '2.0')
    c.add('prodid', '-//Hackerspace OS//code.google.com/p/hackerspace-os//')
    c.add('X-WR-TIMEZONE', 'Europe/Vienna')
    c.add('X-WR-CALNAME', 'Metalab');
    c.add('X-WR-CALDESC', 'Metalab Events Calendar');
    for component in components:
        c.add_component(component)
    return c
