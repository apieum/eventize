# -*- coding: utf8 -*-
from .tools import is_a_method, Method, Attribute
__all__ = ['Observable', 'Observer']


def Observable(cls):
    not_underscored = lambda attr: not attr[0].startswith('_')
    fields = filter(not_underscored, cls.__dict__.items())
    for attr, value in fields:
        setattr(cls, attr, Observer(value))
    return cls

def Observer(value):
    if is_a_method(value):
        return isinstance(value, Method) and value or Method(value)
    return Attribute(value)
