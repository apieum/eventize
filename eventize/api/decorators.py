# -*- coding: utf8 -*-
from ..typing import resolve_type
__all__ = ['Observable', 'Observer']


def Observable(cls):
    not_underscored = lambda attr: not attr[0].startswith('_')
    fields = filter(not_underscored, cls.__dict__.items())
    for attr, value in fields:
        setattr(cls, attr, Observer(value))
    return cls

def Observer(value):
    obs_type = resolve_type(value)
    return value if isinstance(value, obs_type) else obs_type(value)
