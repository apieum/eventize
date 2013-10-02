# -*- coding: utf8 -*-
from method import Method

def ObservedMethod(method):
    return Method(method)

def Observable(cls):
    for attr, value in cls.__dict__.items():
        if attr[0] != '_' and callable(value):
            setattr(cls, attr, Method(value))
    return cls
