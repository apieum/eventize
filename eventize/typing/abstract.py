# -*- coding: utf8 -*-
from abc import ABCMeta

def base_class(cls):
    return ABCMeta(cls.__name__, (cls, ), {})
