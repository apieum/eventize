# -*- coding: utf8 -*-
from .. import events, descriptors
from .event import Event


class Handler(descriptors.Handler):
    event_class = Event

    class handler_class(events.Handler):
        event_class = Event
        def before_propagation(self, event):
            if hasattr(self, 'parent'):
                self.parent(event)

class InstanceHandler(events.Handler):
    event_class = Event


Subject = events.Subject(Handler)
