# -*- coding: utf8 -*-
from . import Method, Attribute
from .tools import is_a_method
__all__ = ['handle', 'on_get', 'on_set', 'on_del', 'before', 'after']

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
