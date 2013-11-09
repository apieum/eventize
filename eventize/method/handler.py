# -*- coding: utf8 -*-
from ..events import EventHandler, Subject
from ..descriptors.handler import DescriptorHandler
from .event import MethodEvent

class MethodHandler(DescriptorHandler):
    event_class = MethodEvent
    def build_instance_handler(self, parent):
        alias = self.get_alias(parent)
        instance_handler = InstanceHandler()
        instance_handler.parent = self
        instance_handler.parentInstance = getattr(parent, alias)
        return instance_handler

class InstanceHandler(EventHandler):
    event_class = MethodEvent

    def before_propagation(self, event):
        if hasattr(self, 'parent'):
            self.parent(event)
        if hasattr(self, 'parentInstance'):
            self.parentInstance(event)

MethodSubject = Subject(MethodHandler)
