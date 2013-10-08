# -*- coding: utf8 -*-

class NamedDescriptor(object):
    __name__ = None
    def _find_name(self, ownerCls):
        for attr, value in list(ownerCls.__dict__.items()):
            if value is self:
                return attr

    def _get_name(self, instance):
        if self.__name__ is None:
            self.__name__ = self._find_name(type(instance))
        return self.__name__
