# -*- coding: utf8 -*-
from .. import descriptors
from .handler import BeforeHandler, AfterHandler
from .value import Value

class Descriptor(descriptors.Named):
    ValueType = Value
    before = BeforeHandler()
    after = AfterHandler()

