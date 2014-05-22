# -*- coding: utf8 -*-
from .. import descriptors
from .handler import Handler
from .value import Value

class Descriptor(descriptors.Named):
    ValueType = Value
    before = Handler()
    after = Handler()

