# -*- coding: utf8 -*-
from .exceptions import StopPropagation

class Event(object):
    def __init__(self, subject, *args, **kwargs):
        self.subject = subject
        self.messages = []
        self.results = []

    def __contains__(self, value):
        return value(self)

    def trigger(self, callback):
        self.results.append(callback(self))

    def stop_propagation(self, msg=None):
        self.messages.append(msg)
        raise StopPropagation(msg)

    def returns(self):
        return self


class AttributeEvent(Event):
    def __init__(self, subject, name, *args):
        super(AttributeEvent, self).__init__(subject, name, *args)
        self.name = name
        value = subject.__dict__.get(name, None)
        if len(args) > 0:
            value = args[0]
        self.value = value

    def returns(self):
        return self.value

GetEvent = AttributeEvent
SetEvent = AttributeEvent
DelEvent = AttributeEvent


class MethodEvent(Event):
    def __init__(self, subject, *args, **kwargs):
        super(MethodEvent, self).__init__(subject, *args, **kwargs)
        self.args = args
        self.kwargs = kwargs
        for key, value in list(kwargs.items()):
            setattr(self, key, value)
        self.result = None

    def call(self, func):
        self.result = func(self.subject, *self.args, **self.kwargs)
        return self.result

    def returns(self):
        return self.result


AfterEvent = MethodEvent
BeforeEvent = MethodEvent
