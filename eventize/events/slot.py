# -*- coding: utf8 -*-

class StopPropagation(UserWarning):
    pass

class Slot(list):
    def __init__(self, *func_list):
        self._assert_list_valid(func_list)
        list.__init__(self, func_list)
        self.message = ''

    def __call__(self, *args, **kwargs):
        result = None
        try:
            result = self.propagate(*args, **kwargs)
        except StopPropagation as reason:
            self.message = reason.message

        return result

    def propagate(self, *args, **kwargs):
        result = None
        for func in self:
            result = func(*args, **kwargs)
        return result

    def when(self, condition):
        from conditional import Conditional
        cond = Conditional(condition=condition)
        self.append(cond)
        return cond

    def called_with(self, *expected_args, **expected_kwargs):
        def condition(*args, **kwargs):
            for arg in expected_args:
                if arg not in args:
                    return False
            for key, item in expected_kwargs.iteritems():
                if key not in kwargs or kwargs[key] is not item:
                    return False
            return True
        return self.when(condition)

    def __iadd__(self, func):
        self.append(func)
        return self

    def __isub__(self, func):
        while func in self:
            self.remove(func)
        return self

    def __setitem__(self, key, func):
        self._assert_valid(func)
        return list.__setitem__.__call__(self, key, func)

    def append(self, func):
        self._assert_valid(func)
        return list.append.__call__(self, func)

    def insert(self, key, func):
        self._assert_valid(func)
        return list.insert.__call__(self, key, func)

    def extend(self, func_list):
        self._assert_list_valid(func_list)
        return list.extend.__call__(self, func_list)

    def _assert_list_valid(self, enumerable):
        for value in enumerable:
            self._assert_valid(value)

    def _assert_valid(self, func):
        if not callable(func):
            raise TypeError('"%s": is not calable' % func)

