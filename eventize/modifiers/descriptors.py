# -*- coding: utf8 -*-
from ..typing import Modifier

class Default(Modifier):
    def __init__(self, value):
        self.value = value

    def visit(self, handler):
        self.old_value = getattr(handler, 'default')
        setattr(handler, 'default', self.value)

    def restore(self, handler):
        setattr(handler, 'default', self.old_value)
