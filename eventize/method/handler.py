# -*- coding: utf8 -*-
from .. import events, descriptors
from .event import Event


class Handler(descriptors.Handler):
    event_class = Event

class InstanceHandler(events.Handler):
    event_class = Event


Subject = events.Subject(Handler)
