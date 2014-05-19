# -*- coding: utf8 -*-
from .named import Named
from .. import events


class Handler(events.Handler, Named):
    handler_class = events.Handler
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


class WrapCondition(object):
    def __init__(self, handlers, condition):
        for handler_name, handler in list(handlers.items()):
            setattr(self, handler_name, handler.when(condition))



Subject = events.Subject(Handler)
