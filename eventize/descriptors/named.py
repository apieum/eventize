# -*- coding: utf8 -*-
from .wrappers import WrapCondition

class Value(object):
    def __init__(self, value, instance=None, alias=''):
        self.instance = instance
        self.ownerCls = getattr(type(instance), alias, None)
        self.name = alias
        attrs_without_handlers = set(self.__dict__.keys())
        self.set_handlers()
        self.event_handlers = set(self.__dict__.keys()) - attrs_without_handlers
        value = self.init_value(value)
        if value is not None:
            self.set(value)


    def set_handlers(self):
        pass

    def init_value(self, value):
        return value

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

    def notify(self, event_name, event):
        self.call(event_name, 'propagate', event)
        return event

    def when(self, condition):
        handlers = {}
        for handler in self.event_handlers:
            handlers[handler] = self.instance_attr(handler)
            handlers["%s_class" % handler] = self.class_attr(handler)
            handlers["%s_descriptor" % handler] = self.descriptor_attr(handler)
        return WrapCondition(handlers, condition)



class Named(object):
    __alias__ = None
    ValueType = Value

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self.default = args[0]
        if 'default' in kwargs:
            self.default = kwargs['default']

    def find_alias(self, ownerCls):
        for attr, value in ownerCls.__dict__.items():
            if value is self:
                return attr

    def get_alias(self, instance):
        if self.__alias__ is None:
            self.__alias__ = self.find_alias(type(instance))
        return self.__alias__

    def get_value(self, instance):
        alias = self.get_alias(instance)
        self.set_default(instance, alias)
        return self.get(instance, alias)

    def __get__(self, instance, ownerCls=None):
        if instance is None: return self
        return self.get_value(instance).get()

    def __set__(self, instance, value):
        if instance is None: return self
        alias = self.get_alias(instance)
        self.set(instance, alias, value)

    def __delete__(self, instance):
        if instance is None: return self
        alias = self.get_alias(instance)
        if self.is_set(instance, alias):
            self.delete(instance, alias)

    def is_set(self, instance, alias):
        return alias in instance.__dict__

    def is_not_set(self, instance, alias):
        return not self.is_set(instance, alias)

    def get(self, instance, alias):
        return instance.__dict__[alias]

    def set(self, instance, alias, value):
        if self.is_set(instance, alias):
            instance.__dict__[alias].set(value)
        else:
            instance.__dict__[alias] = self.ValueType(value, instance, alias)

    def delete(self, instance, alias):
        instance.__dict__[alias].delete()

    def set_default(self, instance, alias):
        if self.is_set(instance, alias): return True
        default = getattr(self, 'default', None)
        setattr(instance, alias, default)
        return default != None


