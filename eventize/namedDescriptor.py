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


    def __get__(self, instance, ownerCls):
        if instance is None: return self
        name = self._get_name(instance)
        return self._retrieve_from_name(name, instance)

    def _retrieve_from_name(self, name, instance):
        raise NotImplementedError("%s._retrieve_from_name must be implemented" % type(self).__name__)
