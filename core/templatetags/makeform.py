import sys
from django import template

register = template.Library()

@register.tag(name="makeform")
def do_makeform(parser, token):
    """ do_makeform variable path.to.form.class target_name """
    try:
        tag_name, context_var, form_path, target_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires two arguments" % token.contents.split()[0]

    try:
        modulename, classname = form_path.rsplit('.',1)
        module = __import__(modulename, fromlist=[classname])
    except:
        raise template.TemplateSyntaxError, "the path to form class (%s) should be import-able! %r" % (form_path.rsplit('.', 1)[0], token.contents.split()[0])

    cls = getattr(module, classname)

    return MakeFormNode(context_var, cls, target_name)

class MakeFormNode(template.Node):
    def __init__(self, context_var, cls, target_name):
        self.context_var = template.Variable(context_var) if context_var != 'None' else None
        self.cls = cls
        self.target_name = target_name

    def render(self, context):
        if self.context_var:
            try:
                actual_var = self.context_var.resolve(context)
            except template.VariableDoesNotExist:
                raise template.TemplateSyntaxError, 'MakeFormNode cannot resolve variable'

        if not self.context_var:
            context[self.target_name]=self.cls()
        else:
            context[self.target_name]=self.cls(instance=actual_var)

        return ''
