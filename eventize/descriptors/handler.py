# -*- coding: utf8 -*-
from .named import Named
from .. import events


class Handler(events.Handler, Named):
    default = events.Handler
    def set_default(self, instance, alias):
        if self.is_set(instance, alias): return False
        handler = self.default(condition=self.condition)
        self.set(instance, alias, handler)
        return True

    def __hash__(self):
        return id(self)


Subject = events.Subject(Handler)
