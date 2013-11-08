# -*- coding: utf8 -*-
from ..descriptors.handler import DescriptorHandler
from ..events import EventHandler, Subject
from .event import AttributeEvent


class AttributeHandler(DescriptorHandler):
    event_class = AttributeEvent
    def instance_handler(self, alias, copy_from=None):
        return getattr(copy_from, alias, InstanceHandler())

    def attach_instance_handler(self, alias, subject, copy_from):
        handler = self.instance_handler(alias, copy_from)
        try:
            setattr(subject, alias, handler)
        except AttributeError:
            subject = self.subtype_subject(subject)
            setattr(subject, alias, handler)
        return subject

    def subtype_subject(self, subject):
        subject_type = type(subject)
        bases = (subject_type, ) + subject_type.__bases__
        attrs = dict(subject_type.__dict__)
        return type(subject_type.__name__, bases, attrs)(subject)

    class handler_class(EventHandler):
        event_class = AttributeEvent
        def before_propagation(self, event):
            if hasattr(self, 'parent'):
                self.parent(event)

        def after_propagation(self, event):
            alias = getattr(self, '__alias__', '')
            handler = getattr(event.value, alias, lambda event: event)
            handler(event)


class InstanceHandler(EventHandler):
    event_class = AttributeEvent


AttributeSubject = Subject(AttributeHandler)
