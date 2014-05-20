# -*- coding: utf8 -*-
from .. import descriptors, events
from .event import Event


class Handler(descriptors.Handler):
    event_class = Event

    class handler_class(events.Handler):
        event_class = Event
        def before_propagation(self, event):
            if hasattr(self, 'parent'):
                self.parent(event)

        def after_propagation(self, event):
            alias = getattr(self, '__alias__', '')
            handler = getattr(event.value, alias, lambda event: event)
            handler(event)


class InstanceHandler(events.Handler):
    event_class = Event


Subject = events.Subject(Handler)
