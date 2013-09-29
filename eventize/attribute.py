# -*- coding: utf8 -*-
from slots import Conditional

class Attribute(object):
    __alias__ = None
    def __init__(self, default = None):
        self.on_get = Conditional('on_get')
        self.on_set = Conditional('on_set')
        self.on_del = Conditional('on_del')
        self.__default = default

    def __find_alias(self, ownerCls):
        for attr, value in ownerCls.__dict__.iteritems():
            if value is self:
                return attr


    def __get_alias(self, instance):
        ownerCls = instance.__class__
        if self.__alias__ is None:
            self.__alias__ = self.__find_alias(ownerCls)
        return self.__alias__

    def __assert_is_set(self, instance, attr):
        if attr not in instance.__dict__:
            cls_name = instance.__class__.__name__
            raise AttributeError("AttributeError: '%s' object has no attribute '%s'" % (cls_name, attr))

    def __get__(self, instance, ownerCls):
        if instance is None:
            return self
        alias = self.__get_alias(instance)
        self.on_get(instance, alias)
        try:
            self.__assert_is_set(instance, alias)
        except AttributeError as error:
            if self.__default is None:
                raise error
            self.__set__(instance, self.__default)

        return instance.__dict__[alias]

    def __set__(self, instance, value):
        alias = self.__get_alias(instance)
        self.on_set(instance, alias, value)
        instance.__dict__[alias] = value

    def __delete__(self, instance):
        alias = self.__get_alias(instance)
        self.on_del(instance, alias)
        if alias in instance.__dict__:
            del instance.__dict__[alias]
