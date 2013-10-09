# -*- coding: utf8 -*-
from .handler import Handler


class Conditional(Handler):
    def __init__(self, *args, **kwargs):
        Handler.__init__(self, *args)
        if 'condition' not in kwargs:
            kwargs['condition'] = lambda event: True
        self._assert_valid(kwargs['condition'])
        self.condition = kwargs['condition']


    def propagate(self, event):
        if not self.condition(event):
            msg = "Condition '%s' for event '%s' return False" % (self.condition, event)
            event.stop_propagation(msg)
        return Handler.propagate(self, event)
