# -*- coding: utf8 -*-
from .slot import StopPropagation

class Event(object):
    def __init__(self, instance, *args, **kwargs):
        self.instance = instance
        self.args = args
        self.kwargs = kwargs
        for key, value in list(kwargs.items()):
            setattr(self, key, value)
        self.result = None
        self.messages = []
        self.results = []

    def call(self, func):
        result = func(self)
        self.results.append(result)
        return result

    def stop_propagation(self, msg=None):
        self.messages.append(msg)
        raise StopPropagation(msg)

    def has_arg(self, value):
        return value == self.instance or value in self.args

    def has_kwarg(self, key, value):
        return hasattr(self, key) and getattr(self, key) == value
