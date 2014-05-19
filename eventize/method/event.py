# -*- coding: utf8 -*-
from .. import events

class Event(events.Event):
    def __init__(self, subject, *args, **kwargs):
        events.Event.__init__(self, subject, *args, **kwargs)
        self.args = args
        self.kwargs = kwargs
        for key, value in list(kwargs.items()):
            setattr(self, key, value)
        self.result = None

    def call(self, func):
        self.result = func(self.subject, *self.args, **self.kwargs)
        return self.returns()

    def returns(self):
        return self.result
