# -*- coding: utf8 -*-
from ..events import Event

class AttributeEvent(Event):
    def __init__(self, subject, name, *args, **kwargs):
        super(AttributeEvent, self).__init__(subject, name, *args)
        self.name = name
        value = subject.__dict__.get(name, None)
        if len(args) > 0:
            value = args[0]
        value = kwargs.get('value', value)
        self.value = value

    def returns(self):
        return self.value
