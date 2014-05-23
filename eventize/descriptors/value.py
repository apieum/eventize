# -*- coding: utf8 -*-
from .wrappers import WrapCondition

class Value(object):
    def __init__(self, value, instance, alias):
        self.instance = instance
        self.ownerCls = getattr(type(instance), alias, None)
        self.name = alias
        attrs_without_handlers = set(self.__dict__.keys())
        self.set_handlers()
        self.event_handlers = set(self.__dict__.keys()) - attrs_without_handlers
        self.init_value(value)

    def set_handlers(self):
        pass

    def init_value(self, value):
        if value is not None:
            self.set(value)

    def get(self):
        return self.data

    def set(self, value):
        self.data = value

    def delete(self):
        delattr(self, 'data')

    def descriptor_attr(self, handler):
        return getattr(type(self.ownerCls), handler)

    def class_attr(self, handler):
        return getattr(self.ownerCls, handler)

    def instance_attr(self, handler):
        return getattr(self, handler)

    def call_all(self, method, *args, **kwargs):
        for handler in self.event_handlers:
            self.call(handler, method, *args, **kwargs)

    def call(self, handler, method, *args, **kwargs):
        getattr(self.descriptor_attr(handler), method)(*args, **kwargs)
        getattr(self.class_attr(handler), method)(*args, **kwargs)
        getattr(self.instance_attr(handler), method)(*args, **kwargs)

    def clear_all(self):
        self.call_all('clear')

    def clear_all_events(self):
        self.call_all('clear_events')

    def notify(self, event_name, *args, **kwargs):
        event = self.instance_attr(event_name).make_event(*args, **kwargs)
        self.call(event_name, 'propagate', event)
        return event

    def when(self, condition):
        handlers = {}
        for handler in self.event_handlers:
            handlers[handler] = self.instance_attr(handler)
            handlers["%s_class" % handler] = self.class_attr(handler)
            handlers["%s_descriptor" % handler] = self.descriptor_attr(handler)
        return WrapCondition(handlers, condition)

