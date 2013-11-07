# -*- coding: utf8 -*-
from .handler import DescriptorHandler
__all__ = ['Subject']


class Subject(object):
    def __new__(cls, decorated):
        bind_null = lambda ownerCls: ownerCls
        handlers = filter(cls.is_handler, decorated.__dict__.items())
        parent = decorated.__bases__[0]
        for alias, handler in handlers:
            parent_handler = parent.__dict__.get(alias, [])
            for observer in parent_handler:
                handler.insert(0, observer)
            bind = getattr(handler, 'bind', bind_null)
            decorated = bind(decorated)
        return decorated

    @classmethod
    def is_handler(cls, attribute):
        return isinstance(attribute[1], DescriptorHandler)

