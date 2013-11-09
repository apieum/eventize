# -*- coding: utf8 -*-
__all__ = ['Subject']


class Subject(object):
    def __init__(self, *handlers_type):
        self.handlers_type = handlers_type

    def __call__(self, decorated):
        bind_null = lambda ownerCls: ownerCls
        handlers = self.filter_handlers(decorated)
        parent = decorated.__bases__[0]
        for alias, handler in handlers:
            handler.prepend(tuple(getattr(parent, alias, [])))
            bind = getattr(handler, 'bind', bind_null)
            decorated = bind(decorated)
        return decorated

    def is_handler(self, attribute):
        return isinstance(attribute[1], self.handlers_type)

    def filter_handlers(self, cls):
        return filter(self.is_handler, cls.__dict__.items())

