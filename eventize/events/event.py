# -*- coding: utf8 -*-

class Event(object):
    __type__ = 'NotSet'
    def __init__(self, subject, *args, **kwargs):
        self.subject = subject
        self.args = args
        self.kwargs = kwargs
        for key, value in list(kwargs.items()):
            setattr(self, key, value)
        self.result = None
        self.messages = []
        self.results = []

    def __contains__(self, value):
        return value(self)

    def call(self, func):
        self.result = func(self.subject, *self.args, **self.kwargs)
        return self.result

    def trigger(self, callback):
        self.results.append(callback(self))

    def stop_propagation(self, msg=None):
        from .handler import StopPropagation
        self.messages.append(msg)
        raise StopPropagation(msg)
