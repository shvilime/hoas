from systemapps.menu.models import Menu, MenuItem
from django import template

register = template.Library()

@register.tag(name='menu')
def buildmenu(parser, token):
    try:
        tag_name, menu_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return MenuObject(menu_name)

class MenuObject(template.Node):
    def __init__(self, menu_name):
        self.menu_name = menu_name

    def render(self, context):
        context['nodes'] = MenuItem.objects.filter(menu__name = self.menu_name)
        return ''

def get_menuitems(menu_name, user):
    menuitems = []

    return menuitems