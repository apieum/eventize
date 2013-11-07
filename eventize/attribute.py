# -*- coding: utf8 -*-
from .namedDescriptor import NamedDescriptor
from .events.handler import AttributeHandler
from .events.subject import Subject

is_handler = lambda handler: isinstance(handler, AttributeHandler)

@Subject
class Attribute(NamedDescriptor):
    on_get = AttributeHandler()
    on_set = AttributeHandler()
    on_del = AttributeHandler()

    def __init__(self, default=None):
        self.default = default

    def get(self, instance, name):
        self._assert_is_set(instance, name)
        event = self.on_get.call(instance, name=name)
        return event.returns()

    def set(self, instance, name, value):
        old_value = instance.__dict__.get(name, None)
        value = self.attach_handlers(value, old_value)
        event = self.on_set.call(instance, name=name, value=value)
        instance.__dict__[event.name] = event.value

    def delete(self, instance, name):
        event = self.on_del.call(instance, name=name)
        del instance.__dict__[event.name]

    def _assert_is_set(self, instance, name):
        if self.is_not_set(instance, name):
            if self.default is None:
                raise AttributeError("'%s' has no attribute '%s'" % (instance, name))
            self.set(instance, name, self.default)

    def attach_handlers(self, subject, copy_from=None):
        this_handlers = list(filter(is_handler, type(self).__dict__.values()))
        try:
            for handler in this_handlers:
                subject = handler.attach_instance_handler(self, subject, copy_from)
        except TypeError:
            pass
        return subject
