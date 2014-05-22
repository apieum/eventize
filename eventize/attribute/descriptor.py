# -*- coding: utf8 -*-
from .. import descriptors
from .handler import Handler, Subject
from .value import Value

@Subject
class Descriptor(descriptors.Named):
    ValueType = Value
    on_get = Handler()
    on_set = Handler()
    on_del = Handler()
    on_change = Handler()
