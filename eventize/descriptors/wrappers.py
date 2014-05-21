# -*- coding: utf8 -*-


class WrapCondition(object):
    def __init__(self, handlers, condition):
        for handler_name, handler in list(handlers.items()):
            setattr(self, handler_name, handler.when(condition))


