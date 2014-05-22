# -*- coding: utf8 -*-
from .. import events

class BeforeEvent(events.Event):
    def __init__(self, subject, *args, **kwargs):
        events.Event.__init__(self, subject.instance)
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
        events.Event.__init__(self, event.subject)
        self.args = event.args
        self.kwargs = event.kwargs
        self.result = event.returns()

    def returns(self):
        return self.result
