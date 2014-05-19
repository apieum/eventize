# -*- coding: utf8 -*-
from .. import descriptors
from .handler import Handler, Subject

@Subject
class Descriptor(descriptors.Named):
    on_get = Handler()
    on_set = Handler()
    on_del = Handler()

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
        descriptors.Named.delete(self, event.subject, event.name)

    def attach_handlers(self, subject, copy_from=None):
        this_handlers = Subject.filter_handlers(type(self))
        try:
            for handler_name, handler in this_handlers:
                subject = handler.attach_instance_handler(handler_name, subject, copy_from)
        except TypeError:
            pass
        return subject
