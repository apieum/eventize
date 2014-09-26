# -*- coding: utf8 -*-
from ..typing import Modifier

class EventType(Modifier):
    def __init__(self, event_type):
        self.event_type = event_type

    def visit(self, handler):
        self.old_event = getattr(handler, 'event_type')
        setattr(handler, 'event_type', self.event_type)

    def restore(self, handler):
        setattr(handler, 'event_type', self.old_event)
