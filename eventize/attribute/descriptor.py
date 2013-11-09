# -*- coding: utf8 -*-
from ..descriptors import NamedDescriptor
from .handler import AttributeHandler, AttributeSubject

@AttributeSubject
class Attribute(NamedDescriptor):
    on_get = AttributeHandler()
    on_set = AttributeHandler()
    on_del = AttributeHandler()

    def get_result(self, instance, name, value):
        event = self.on_get.trigger(instance, name=name, value=value)
        return event.returns()

    def set_args(self, instance, name, value):
        old_value = self.get(instance, name, None)
        value = self.attach_handlers(value, old_value)
        event = self.on_set.trigger(instance, name=name, value=value)
        return event.subject, event.name, event.value

    def delete(self, instance, name):
        event = self.on_del.trigger(instance, name=name)
        NamedDescriptor.delete(self, event.subject, event.name)

    def attach_handlers(self, subject, copy_from=None):
        this_handlers = AttributeSubject.filter_handlers(type(self))
        try:
            for handler_name, handler in this_handlers:
                subject = handler.attach_instance_handler(handler_name, subject, copy_from)
        except TypeError:
            pass
        return subject
