# -*- coding: utf8 -*-
from .exceptions import StopPropagation

class Event(object):
    def __init__(self, subject, *args, **kwargs):
        self.subject = subject
        self.messages = []
        self.results = []

    def trigger(self, callback):
        self.results.append(callback(self))

    def stop_propagation(self, msg=None):
        self.messages.append(msg)
        raise StopPropagation(msg)

    def returns(self):
        return self



