# -*- coding: utf8 -*-
from .. import events, descriptors


class Handler(descriptors.Handler):
    pass

class InstanceHandler(events.Handler):
    pass


Subject = events.Subject(Handler)
