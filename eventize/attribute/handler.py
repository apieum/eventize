# -*- coding: utf8 -*-
from .. import descriptors, events
from .event import Event


class Handler(descriptors.Handler):
    event_class = Event

class InstanceHandler(events.Handler):
    event_class = Event


Subject = events.Subject(Handler)
