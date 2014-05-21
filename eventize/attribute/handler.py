# -*- coding: utf8 -*-
from .. import descriptors, events


class Handler(descriptors.Handler):
    pass

class InstanceHandler(events.Handler):
    pass


Subject = events.Subject(Handler)
