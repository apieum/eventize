# -*- coding: utf8 -*-
from .. import events

class BeforeEvent(events.Event):
    def __init__(self, subject, *args, **kwargs):
        events.Event.__init__(self)
        self.subject = subject.instance
        self.name = subject.name
        self.args = args
        self.kwargs = kwargs
        self.result = None

    def call(self, func):
        self.result = func(self.subject, *self.args, **self.kwargs)
        return self.returns()

    def returns(self):
        return self.result

class AfterEvent(events.Event):
    def __init__(self, event):
        events.Event.__init__(self)
        for attr in ('subject', 'name', 'args', 'kwargs'):
            setattr(self, attr, getattr(event, attr))
        self.result = event.returns()

    def returns(self):
        return self.result
