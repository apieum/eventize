# -*- coding: utf8 -*-
from .named import Named as NamedDescriptor
from ..events import EventHandler, Subject


class DescriptorHandler(EventHandler, NamedDescriptor):
    handler_class = EventHandler
    def set_default(self, instance, alias):
        handler = self.make_handler(instance, alias)
        self.set(instance, alias, handler)

    def make_handler(self, instance, alias):
        handler = self.handler_class(condition=self.condition)
        handler.__alias__ = alias
        handler.parent = self
        return handler

    def __hash__(self):
        return id(self)


DescriptorSubject = Subject(DescriptorHandler)
