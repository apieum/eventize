# -*- coding: utf8 -*-
from .namedDescriptor import NamedDescriptor
from .events.handler import OnGetHandler, OnSetHandler, OnDelHandler

class Attribute(NamedDescriptor):
    on_get = OnGetHandler()
    on_set = OnSetHandler()
    on_del = OnDelHandler()

    def __init__(self, default=None):
        self.default = default

    def get(self, instance, name):
        self._assert_is_set(instance, name)
        event = self.on_get.call(instance, name=name)
        return event.value

    def set(self, instance, name, value):
        event = self.on_set.call(instance, name=name, value=value)
        instance.__dict__[event.name] = event.value

    def delete(self, instance, name):
        event = self.on_del.call(instance, name=name)
        del instance.__dict__[event.name]

    def _assert_is_set(self, instance, name):
        if not self.is_set(instance, name):
            if self.default is None:
                raise AttributeError("'%s' has no attribute '%s'" % (instance, name))
            self.set(instance, name, self.default)


    def clear(self):
        self.on_get.remove_all()
        self.on_set.remove_all()
        self.on_del.remove_all()
