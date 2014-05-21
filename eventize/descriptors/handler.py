# -*- coding: utf8 -*-
from .named import Named
from .. import events


class Handler(events.Handler, Named):
    handler_class = events.Handler
    def set_default(self, instance, alias):
        if self.is_set(instance, alias): return False
        handler = self.make_handler(instance, alias)
        self.set(instance, alias, handler)
        return True

    def make_handler(self, instance, alias):
        return self.handler_class(condition=self.condition)

    def __hash__(self):
        return id(self)


class WrapCondition(object):
    def __init__(self, handlers, condition):
        for handler_name, handler in list(handlers.items()):
            setattr(self, handler_name, handler.when(condition))



Subject = events.Subject(Handler)
