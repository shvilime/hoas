from systemapps.menu.models import Menu, MenuItem
from django import template

register = template.Library()

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
        MenuItem.objects.filter(menu = self.menu_name)
        return ''

register.tag('menu',buildmenu)