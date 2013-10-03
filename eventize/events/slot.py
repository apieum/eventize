# -*- coding: utf8 -*-

class StopPropagation(UserWarning):
    pass

class Slot(list):
    def __init__(self, *args):
        self.__assert_list_valid(args)
        list.__init__(self, args)
        self.message = ''

    def __call__(self, *args, **kwargs):
        result = None
        try:
            result = self.__propagate(args, kwargs)
        except StopPropagation as reason:
            self.message = reason.message

        return result

    def __propagate(self, args, kwargs):
        result = None
        for func in self:
            result = func(*args, **kwargs)
        return result

    def __iadd__(self, func):
        self.append(func)
        return self

    def __isub__(self, func):
        while func in self:
            self.remove(func)
        return self

    def __setitem__(self, key, value):
        self.__assert_valid(value)
        return list.__setitem__.__call__(self, key, value)

    def append(self, value):
        self.__assert_valid(value)
        return list.append.__call__(self, value)

    def insert(self, key, value):
        self.__assert_valid(value)
        return list.insert.__call__(self, key, value)

    def extend(self, value):
        self.__assert_list_valid(value)
        return list.extend.__call__(self, value)

    def __assert_list_valid(self, enumerable):
        for value in enumerable:
            self.__assert_valid(value)

    def __assert_valid(self, value):
        if not callable(value):
            raise TypeError('"%s": is not calable' % value)

