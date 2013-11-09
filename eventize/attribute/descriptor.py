# -*- coding: utf8 -*-
from ..descriptors import NamedDescriptor
from .handler import AttributeHandler, AttributeSubject

@AttributeSubject
class Attribute(NamedDescriptor):
    on_get = AttributeHandler()
    on_set = AttributeHandler()
    on_del = AttributeHandler()

    def __init__(self, default=None):
        self.default = default

    def set_default(self, instance, name):
        if self.default is None:
            super(type(self), self).set_default(instance, name)
        self.set(instance, name, self.default)

    def result(self, instance, name, value):
        event = self.on_get.call(instance, name=name, value=value)
        return event.returns()

    def set(self, instance, name, value):
        old_value = instance.__dict__.get(name, None)
        value = self.attach_handlers(value, old_value)
        event = self.on_set.call(instance, name=name, value=value)
        super(type(self), self).set(event.subject, event.name, event.value)

    def delete(self, instance, name):
        event = self.on_del.call(instance, name=name)
        del instance.__dict__[event.name]

    def attach_handlers(self, subject, copy_from=None):
        this_handlers = AttributeSubject.filter_handlers(type(self))
        try:
            for handler_name, handler in this_handlers:
                subject = handler.attach_instance_handler(handler_name, subject, copy_from)
        except TypeError:
            pass
        return subject
