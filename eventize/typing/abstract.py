# -*- coding: utf8 -*-
from abc import ABCMeta, abstractmethod, abstractproperty

def abstract(cls):
    return ABCMeta(cls.__name__, (cls, ), dict(cls.__dict__))
