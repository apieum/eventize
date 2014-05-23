# -*- coding: utf8 -*-
from .. import events

class Event(events.Event):
    def __init__(self, subject, **kwargs):
        events.Event.__init__(self)
        self.subject = subject.instance
        self.name = subject.name
        if hasattr(subject, 'data'):
            self.value = subject.data
        for arg_name, arg_value in list(kwargs.items()):
            setattr(self, arg_name, arg_value)

    def returns(self):
        return self.value

class OnGetEvent(Event):
    pass

class OnSetEvent(Event):
    pass

class OnDelEvent(Event):
    pass


class OnChangeEvent(events.Event):
    def __init__(self, event):
        events.Event.__init__(self)
        self.subject = event.subject
        self.name = event.name
        self.value = event.returns()

    def returns(self):
        return self.value
