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
        self.result = func(self.instance, *self.args, **self.kwargs)
        return self.result

    def trigger(self, callback):
        self.results.append(callback(self))

    def stop_propagation(self, msg=None):
        self.messages.append(msg)
        raise StopPropagation(msg)

    def arg_equal(self, value):
        return value == self.instance or value in self.args

    def kwarg_equal(self, key, value):
        return hasattr(self, key) and getattr(self, key) == value

    def is_kwarg_instance_of(self, key, *expected_type):
        return hasattr(self, key) and isinstance(getattr(self, key), expected_type)

    def is_kwarg_type_equal(self, key, *expected_types):
        return hasattr(self, key) and type(getattr(self, key)) in expected_types
