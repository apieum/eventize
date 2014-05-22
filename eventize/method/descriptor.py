# -*- coding: utf8 -*-
from .. import descriptors
from .handler import Handler, Subject
from .value import Value

@Subject
class Descriptor(descriptors.Named):
    ValueType = Value
    before = Handler()
    after = Handler()

