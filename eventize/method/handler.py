# -*- coding: utf8 -*-
from .. import events, descriptors
from .event import BeforeEvent, AfterEvent

class Before(events.Handler):
    event_type = BeforeEvent

class After(events.Handler):
    event_type = AfterEvent


class BeforeHandler(descriptors.Handler):
    __alias__ = 'before'
    default = Before

class AfterHandler(descriptors.Handler):
    __alias__ = 'after'
    default = After

Subject = events.Subject(BeforeHandler, AfterHandler)
