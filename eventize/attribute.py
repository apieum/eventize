# -*- coding: utf8 -*-
from .events import Listener
from .namedDescriptor import NamedDescriptor

class Attribute(NamedDescriptor, Listener):
    __events__ = ['on_get', 'on_set', 'on_del']
    def __init__(self, default=None):
        self._set_events(self)
        self.default = default

    def _retrieve_from_name(self, name, instance):
        self._assert_is_set(instance, name)

        event = self._make_event(instance, name=name, value=instance.__dict__[name])
        self.trigger('on_get', event)
        if hasattr(event.value, 'trigger'):
            event.value.trigger('on_get', event)
        return event.value

    def __set__(self, instance, value):
        name = self._get_name(instance)
        old_value = instance.__dict__.get(name, None)
        value = self._set_events(value, old_value)
        event = self._make_event(instance, name=name, value=value)
        self.trigger('on_set', event)
        if old_value is not None and hasattr(event.value, 'trigger'):
            event.value.trigger('on_set', event)

        event.instance.__dict__[event.name] = event.value

    def __delete__(self, instance):
        name = self._get_name(instance)
        if name in instance.__dict__:
            event = self._make_event(instance, name=name, value=instance.__dict__[name])
            self.trigger('on_del', event)
            if hasattr(event.value, 'trigger'):
                event.value.trigger('on_del', event)
            del event.instance.__dict__[name]

    def _assert_is_set(self, instance, name):
        if name not in instance.__dict__:
            if self.default is None:
                raise AttributeError("'%s' has no attribute '%s'" % (instance, name))
            self.__set__(instance, self.default)

