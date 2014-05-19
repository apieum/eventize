# -*- coding: utf8 -*-
from .. import events, descriptors
from .event import Event

class Handler(descriptors.Handler):
    event_class = Event
    def build_instance_handler(self, parent):
        alias = self.get_alias(parent)
        instance_handler = InstanceHandler()
        instance_handler.parent = self
        instance_handler.parentInstance = getattr(parent, alias)
        return instance_handler

class InstanceHandler(events.Handler):
    event_class = Event

    def before_propagation(self, event):
        if hasattr(self, 'parent'):
            self.parent(event)
        if hasattr(self, 'parentInstance'):
            self.parentInstance(event)

Subject = events.Subject(Handler)
