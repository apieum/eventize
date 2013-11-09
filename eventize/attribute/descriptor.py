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
            return NamedDescriptor.set_default(self, instance, name)
        setattr(instance, name, self.default)

    def get_result(self, instance, name, value):
        event = self.on_get.call(instance, name=name, value=value)
        return event.returns()

    def set_args(self, instance, name, value):
        old_value = self.get(instance, name, None)
        value = self.attach_handlers(value, old_value)
        event = self.on_set.call(instance, name=name, value=value)
        return event.subject, event.name, event.value

    def delete(self, instance, name):
        event = self.on_del.call(instance, name=name)
        NamedDescriptor.delete(self, event.subject, event.name)

    def attach_handlers(self, subject, copy_from=None):
        this_handlers = AttributeSubject.filter_handlers(type(self))
        try:
            for handler_name, handler in this_handlers:
                subject = handler.attach_instance_handler(handler_name, subject, copy_from)
        except TypeError:
            pass
        return subject
