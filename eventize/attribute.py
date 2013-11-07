# -*- coding: utf8 -*-
from .namedDescriptor import NamedDescriptor
from .events.event import AttributeEvent
from .events.handler import AttributeHandler, Handler
from .events.subject import Subject

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
        value = self.set_events(value, old_value)
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

    def set_events(self, subject, copy_from=None):
        handlers = {'on_get': None, 'on_set': None, 'on_del': None,}
        for handler_name in handlers.keys():
            handlers[handler_name] = getattr(copy_from, handler_name, Handler())
            handlers[handler_name].event_class = AttributeEvent
        try:
            self.attach_handlers(subject, handlers)
        except AttributeError:
            subject = self.subtype_subject(subject, **handlers)
        return subject

    def attach_handlers(self, subject, handlers):
        for handler_name, handler in handlers.items():
            setattr(subject, handler_name, handler)

    def subtype_subject(self, subject, **handlers):
        subject_type = type(subject)
        bases = (subject_type, ) + subject_type.__bases__
        attrs = dict(subject_type.__dict__)
        try:
            subject = type(subject_type.__name__, bases, attrs)(subject)
            self.attach_handlers(subject, handlers)
        except TypeError:
            pass
        return subject
