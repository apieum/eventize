# -*- coding: utf8 -*-
from .named import Named
from .. import events


class Handler(events.Handler, Named):
    default = events.Handler
    def set_default(self, instance, alias):
        if self.is_set(instance, alias): return
        handler = self.default(condition=self.condition)
        instance.__dict__[alias] = self.ValueType(handler, instance, alias)

    def __hash__(self):
        return id(self)


Subject = events.Subject(Handler)
