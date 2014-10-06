# -*- coding: utf8 -*-
from ..typing import resolve_type
__all__ = ['observable', 'observer']


def observable(cls):
    not_underscored = lambda attr: not attr[0].startswith('_')
    fields = filter(not_underscored, cls.__dict__.items())
    for attr, value in fields:
        setattr(cls, attr, observer(value))
    return cls

def observer(value):
    obs_type = resolve_type(value)
    return value if isinstance(value, obs_type) else obs_type(value)
