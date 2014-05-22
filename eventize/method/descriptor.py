# -*- coding: utf8 -*-
from .. import descriptors
from .handler import Before, After
from .value import Value

class Descriptor(descriptors.Named):
    ValueType = Value
    before = Before()
    after = After()

