# -*- coding: utf8 -*-
from .event import Event
__all__ = ['Conditions', 'expect']

class Conditions(list):
    def __init__(self, *args):
        list.__init__(self, args)

    def __call__(self, event):
        if not isinstance(event, Event):
            raise TypeError('First argument must be an Event')
        for expected in self:
            if expected not in event:
                return False
        return True

    def __or__(self, condition):
        return type(self)(lambda event: self(event) or condition(event))
    __ror__ = __or__

    def __and__(self, condition):
        if isinstance(condition, list):
            self.extend(condition)
        else:
            self.append(condition)
        return self
    __rand__ = __and__



class _ExpectDescriptor(object):
    format_return = Conditions
    def equal_to(self, expected, getter=None):
        find = self.get_finder(getter)
        return self.format_return(lambda event: find(event) == expected)
    __eq__ = equal_to

    def not_equal_to(self, expected, getter=None):
        find = self.get_finder(getter)
        return self.format_return(lambda event: find(event) != expected)
    __ne__ = not_equal_to

    def lower_than(self, expected, getter=None):
        find = self.get_finder(getter)
        return self.format_return(lambda event: find(event) < expected)
    __lt__ = lower_than

    def greater_than(self, expected, getter=None):
        find = self.get_finder(getter)
        return self.format_return(lambda event: find(event) > expected)
    __gt__ = greater_than


    def lower_or_equal_than(self, expected, getter=None):
        find = self.get_finder(getter)
        return self.format_return(lambda event: find(event) <= expected)
    __le__ = lower_or_equal_than

    def greater_or_equal_than(self, expected, getter=None):
        find = self.get_finder(getter)
        return self.format_return(lambda event: find(event) >= expected)
    __ge__ = greater_or_equal_than

    def same_as(self, expected, getter=None):
        find = self.get_finder(getter)
        return self.format_return(lambda event: find(event) is expected)

    def type_is(self, expected_type, getter=None):
        getter = self.get_finder(getter)
        find = lambda event: type(getter(event))
        return self.format_return(self.equal_to(expected_type, find))

    def instance_of(self, expected_types, getter=None):
        find = self.get_finder(getter)
        return self.format_return(lambda event: isinstance(find(event), expected_types))

    def __get__(self, instance, ownerCls):
        return self


class _ExpectProperty(_ExpectDescriptor):
    def __init__(self, property_name, getter=None):
        if not callable(getter):
            getter = lambda instance, default=None: getattr(instance, property_name, default)

        self.get_finder = lambda find=getter: callable(find) and find or getter
        self.new = lambda new_getter=None, cls=type(self): cls(property_name, new_getter)


class _ExpectMethod(_ExpectProperty):
    def __call__(self, expected):
        return self.equal_to(expected)


class _ExpectSameMethod(_ExpectMethod):
    def __call__(self, expected):
        return self.same_as(expected)


class _ExpectListMethod(_ExpectProperty):
    def __call__(self, *expected_values):
        return self.contains(expected_values)

    def contains(self, expected_values, getter=None):
        find = self.get_finder(getter)
        def test(event):
            test_list = find(event)
            for value in expected_values:
                if value not in test_list:
                    return False
            return True
        return self.format_return(test)


class _ExpectListItemMethod(_ExpectListMethod):
    def __call__(self, expected_value):
        return self.contains([expected_value])

    def at(self, position, getter=None):
        getter = self.get_finder(getter)
        find = lambda event: getter(event)[position]
        return self.new(find, _ExpectMethod)


class _ExpectDictMethod(_ExpectListMethod):
    def __call__(self, **expected_items):
        return self.contains_items(expected_items)

    def contains_items(self, expected_items, getter=None):
        find = self.get_finder(getter)
        def test(event):
            test_dict = find(event)
            for name, value in expected_items.items():
                if name not in test_dict or value != test_dict[name]:
                    return False
            return True
        return self.format_return(test)


class _ExpectDictItemProperty(_ExpectDictMethod):
    def __call__(self, name, value):
        return self.contains_items({name:value})

    def at(self, key, getter=None):
        getter = self.get_finder(getter)
        find = lambda event, default=None: getter(event).get(key, default)
        return self.new(find, _ExpectMethod)


class __Expect(object):
    kwarg = _ExpectDictItemProperty('kwargs')
    kwargs = _ExpectDictMethod('kwargs')

    arg = _ExpectListItemMethod('args')
    args = _ExpectListMethod('args')

    subject = _ExpectSameMethod('subject')
    result = _ExpectMethod('result')
    name = _ExpectMethod('name')
    value = _ExpectMethod('value')



expect = __Expect()
