# -*- coding: utf8 -*-
from .method.descriptor import Method
from .attribute.descriptor import Attribute
from types import BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType

__all__ = ['Observable', 'Observer', 'handle', 'on_get', 'on_set', 'on_del', 'before', 'after']


def Observable(cls):
    not_underscored = lambda attr: not attr[0].startswith('_')
    fields = filter(not_underscored, cls.__dict__.items())
    for attr, value in fields:
        setattr(cls, attr, Observer(value))
    return cls

def Observer(value):
    if is_a_method(value):
        return Method(value)
    return Attribute(value)

methods = (Method, BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType)
is_a_method = lambda method: isinstance(method, methods)

def handle(obj, name, handler_type=None):
    cls = isinstance(obj, type) and obj or type(obj)
    cls_field = getattr(cls, name)
    if handler_type is None:
        handler_type = is_a_method(cls_field) and Method or Attribute
    if not isinstance(cls_field, handler_type):
        setattr(cls, name, handler_type(cls_field))
    return getattr(obj, name)


def handler_with_event(event_name, handler_type=None):
    return lambda obj, name, handler_type=handler_type: getattr(handle(obj, name, handler_type), event_name)

on_get = handler_with_event('on_get', Attribute)
on_set = handler_with_event('on_set', Attribute)
on_del = handler_with_event('on_del', Attribute)
before = handler_with_event('before', Method)
after  = handler_with_event('after', Method)
