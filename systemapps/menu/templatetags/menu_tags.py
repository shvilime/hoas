import copy
from ast import literal_eval as create_tuple
from importlib import import_module
from systemapps.menu.models import Menu, MenuItem
from django import template
from django.core.exceptions import ImproperlyConfigured
from django.core.cache import cache

register = template.Library()


@register.tag(name='menu')
def build_menu(parser, token):
    try:
        tag_name, menu_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return MenuObject(menu_name)


class MenuObject(template.Node):
    def __init__(self, menu_name):
        self.menu_name = menu_name
        self.request = None

    def get_menuitems(self):
        from django.conf import settings
        cache_time = getattr(settings, 'MENU_CACHE_TIME', 1800)
        debug = getattr(settings, 'DEBUG', False)
        cache_key = 'menu-items/{menu_name}'.format(menu_name=self.menu_name)

        menuitems = []
        if cache_time >= 0 and not debug:
            menuitems = cache.get(cache_key, [])
        if not menuitems:
            menuitems = MenuItem.objects.filter(menu__name=self.menu_name)
            if cache_time >= 0 and not debug:
                cache.set(cache_key, menuitems, cache_time)

        return menuitems

    def get_callable(self, func_or_path):
        # Receives a dotted path or a callable, Returns a callable or None
        if callable(func_or_path):
            return func_or_path
        module_name = '.'.join(func_or_path.split('.')[:-1])
        function_name = func_or_path.split('.')[-1]
        _module = import_module(module_name)
        func = getattr(_module, function_name)
        return func

    def is_validated(self, menuitem):
        try:
            validators = create_tuple(menuitem.validators)
        except (ValueError, SyntaxError):
            validators = None

        if not validators:
            return True
        if not isinstance(validators, (list, tuple)):
            raise ImproperlyConfigured("validators must be a list")

        result_validations = []
        for validator in validators:
            if isinstance(validator, tuple):
                if len(validator) <= 1:
                    raise ImproperlyConfigured("You are passing a tuple validator without args %s" % str(validator))
                func = self.get_callable(validator[0])
                # Using a python slice to get all items after the first to build function args
                args = validator[1:]
                # Pass the request as first arg by default
                result_validations.append(func(self.request, *args))
            else:
                func = self.get_callable(validator)
                result_validations.append(func(self.request))  # pragma: no cover
        return all(result_validations)

    def validate_menu(self):
        # A generator thet return validated menuitem only.
        for menuitem in self.get_menuitems():
            if self.is_validated(menuitem):
                yield copy.copy(menuitem)

    def generate_menu(self):
        visible_menu = []
        for item in self.validate_menu():
            visible_menu.append(item)
        return visible_menu

    def render(self, context):
        self.request = context['request']
        context['nodes'] = self.generate_menu()
        return ''
