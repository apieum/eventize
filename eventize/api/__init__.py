# -*- coding: utf8 -*-
from .decorators import observable, observer
from .constructors import handle, on_get, on_set, on_del, on_change, before, after, set_handler_type

# kept for compatibility with previous versions
Observer = observer
Observable = observable

__all__ = ['Observable', 'Observer','observable', 'observer', 'handle', 'on_get', 'on_set', 'on_del', 'on_change', 'before', 'after', 'set_handler_type']
