from django import template
from django.template import Variable
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from mos.cal.models import Event
from mos.core.models import Location, Category


register = template.Library()


@register.tag(name="events_by_type")
def do_events_by_type(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly two arguments" % token.contents.split()[0]
    return EventsByTypeNode(name)


class EventsByTypeNode(template.Node):
    def __init__(self, name):
        self.obj = Variable(name)

    def render(self, context):
        kw = self.obj.resolve(context).__class__.__name__.lower() + '__name' 
        filter_arg = {str(kw): self.obj.resolve(context).name}
        obj_sub_list = Event.objects.filter(**filter_arg)     
        context['latestevents'] = obj_sub_list
        return ''

