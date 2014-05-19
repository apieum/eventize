# -*- coding: utf8 -*-
from .. import events

class Event(events.Event):
    def __init__(self, subject, name, *args, **kwargs):
        events.Event.__init__(self, subject, name, *args)
        self.name = name
        value = subject.__dict__.get(name, None)
        if len(args) > 0:
            value = args[0]
        value = kwargs.get('value', value)
        self.value = value

    def returns(self):
        return self.value
