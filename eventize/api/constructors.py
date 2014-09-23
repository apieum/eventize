# -*- coding: utf8 -*-
from .typing import is_a_method, resolve_type

__all__ = ['handle', 'on_get', 'on_set', 'on_del', 'on_change', 'before', 'after', 'set_handler_type']

def handle(obj, name, handler_type=None):
    if isinstance(obj, type):
        return _handle_cls(obj, name, handler_type)
    return _handle_obj(obj, name, handler_type)

def _handle_obj(obj, name, handler_type):
    cls_field = _handle_cls(type(obj), name, handler_type)
    return cls_field.get_value(obj)

def _handle_cls(cls, name, handler_type):
    cls_field = getattr(cls, name)
    handler_type = resolve_type(cls_field, handler_type)
    if not isinstance(cls_field, handler_type):
        cls_field = set_handler_type(cls, name, handler_type)
    return cls_field

def set_handler_type(cls, name, handler_type):
    cls_field = getattr(cls, name)
    default = getattr(cls_field, 'default', cls_field)
    cls_field = handler_type(default=default)
    setattr(cls, name, cls_field)
    return cls_field

def handle_event(event_name):
    def handle_event(obj, name, handler_type=None):
        return getattr(handle(obj, name, handler_type), event_name)
    return handle_event

on_get = handle_event('on_get')
on_set = handle_event('on_set')
on_del = handle_event('on_del')
on_change = handle_event('on_change')
before = handle_event('before')
after  = handle_event('after')
