# -*- coding: utf8 -*-
from ..typing import Modifier

class Default(Modifier):
    def __init__(self, value):
        self.value = value
        self.old_value = None

    def visit(self, handler):
        self.old_value = handler.__dict__.get('default', None)
        handler.__dict__['default'] = self.value

    def restore(self, handler):
        handler.__dict__['default'] = self.old_value
