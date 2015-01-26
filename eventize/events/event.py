# -*- coding: utf8 -*-
from .exceptions import StopPropagation
from ..typing import AbstractEvent

class Event(AbstractEvent):
    def __init__(self, *args, **kwargs):
        self.args = args
        for name, value in list(kwargs.items()):
            setattr(self, name, value)
        if getattr(self, '__channel__', None) is None:
            setattr(self, '__channel__', type(self).__name__)
        self.messages = []
        self.results = []

    def trigger(self, callback):
        self.results.append(callback(self))

    def stop_propagation(self, msg=None):
        self.messages.append(msg)
        raise StopPropagation(msg)

    def returns(self):
        return self
