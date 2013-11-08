# -*- coding: utf8 -*-
from .named import Named as NamedDescriptor
from ..events import EventHandler, Subject


class DescriptorHandler(EventHandler, NamedDescriptor):
    handler_class = EventHandler
    def get(self, instance, alias):
        if not self.is_set(instance, alias):
            instance.__dict__[alias] = self.make_handler(instance, alias)
        return instance.__dict__[alias]

    def set(self, instance, alias, value):
        instance.__dict__[alias] = value

    def delete(self, instance, alias):
        del instance.__dict__[alias]

    def make_handler(self, instance, alias):
        handler = self.handler_class(condition=self.condition)
        handler.__alias__ = alias
        handler.parent = self
        return handler

    def __hash__(self):
        return id(self)



DescriptorSubject = Subject(DescriptorHandler)
