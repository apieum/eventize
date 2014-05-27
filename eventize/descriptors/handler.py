# -*- coding: utf8 -*-
from .named import Named
from .. import events
from .value import Value


class Handler(events.Handler, Named):
    default = events.Handler
    class ValueType(Value):
        def init_value(self, value):
            super(type(self), self).init_value(None)
            self.set(value())

    def __hash__(self):
        return id(self)


Subject = events.Subject(Handler)
