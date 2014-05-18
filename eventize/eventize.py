# -*- coding: utf8 -*-
from .method.descriptor import Method
from .attribute.descriptor import Attribute
from types import BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType

__all__ = ['Observable', 'Observer', 'handle']


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

methods = (BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType)
is_a_method = lambda method: isinstance(method, methods)

def handle(obj, name):
    cls = isinstance(obj, type) and obj or type(obj)
    cls_field = getattr(cls, name)
    if not isinstance(cls_field, (Method, Attribute)):
        setattr(cls, name, Observer(cls_field))
    return getattr(obj, name)
