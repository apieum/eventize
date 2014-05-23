# -*- coding: utf8 -*-

class Subject(object):
    def __init__(self, *handlers_type):
        self.handlers_type = handlers_type

    def __call__(self, decorated):
        bind_null = lambda ownerCls: ownerCls
        handlers = self.filter_handlers(decorated)
        for parent in reversed(decorated.__bases__):
            decorated = self.bind_parent(decorated, parent, handlers)
        return decorated

    def bind_parent(self, decorated, parent, handlers):
        for alias, handler in handlers:
            decorated = self.bind(decorated, handler, getattr(parent, alias, []))
        return decorated

    def bind(self, decorated, handler, data):
        handler.prepend(tuple(data))
        bind = getattr(handler, 'bind', self.bind_null)
        return bind(decorated)

    def bind_null(self, decorated):
        return decorated

    def is_handler(self, attribute):
        return isinstance(attribute[1], self.handlers_type)

    def filter_handlers(self, cls):
        return set(filter(self.is_handler, cls.__dict__.items()))

