# -*- coding: utf8 -*-
import unittest
from mock import Mock
from eventize.method import Method
from eventize.events.event import Event

class MethodTest(unittest.TestCase):
    def test_method_is_a_callable_object(self):
        self.assertTrue(callable(Method))

    def test_method_take_an_argument(self):
        with self.assertRaises(TypeError) as context:
            Method()
        self.assertEqual(context.exception.message, "__init__() takes exactly 2 arguments (1 given)")

    def test_method_argument_must_be_callable(self):
        with self.assertRaises(AttributeError) as context:
            Method("arg")
        self.assertEqual(context.exception.message, '"arg" is not callable')

    def test_method_argument_is_called_when_object_is_called(self):
        mock = Mock()
        meth = Method(mock)
        meth("arg", kwarg="kwarg")
        mock.assert_called_once_with(meth, "arg", kwarg="kwarg")


    def test_method_call_returns_func_argument_result(self):
        expected_returns = "foo"
        mock = Mock(return_value=expected_returns)
        meth = Method(mock)
        self.assertEqual(expected_returns, meth())

    def test_callables_attached_to_before_event_are_called_with_event(self):
        mock = Mock()
        on_meth = Mock()
        meth = Method(mock)
        meth.before += on_meth

        meth("arg", kwarg="kwarg")
        event = meth.before.events[0]
        on_meth.assert_called_once_with(event)

    def test_before_event_can_modify_args(self):
        mock = Mock()
        expected_args = ["mod_arg"]
        expected_kwargs = {'kwargs':"mod_kwarg"}
        def before_meth(event):
            event.args = expected_args
            event.kwargs = expected_kwargs
        event = Event(mock, "arg", kwarg="kwarg")
        meth = Method(mock)
        meth.before += before_meth
        meth.before(event)

        self.assertEqual(expected_args, event.args)
        self.assertEqual(expected_kwargs, event.kwargs)

    def test_callables_attached_to_after_event_are_called_with_event(self):
        mock = Mock(return_value="result")
        after_meth = Mock()
        meth = Method(mock)
        meth.after += after_meth

        meth("arg", kwarg="kwarg")

        after_meth.assert_called_once_with(meth.after.events[0])


    def test_after_event_can_modify_result(self):
        mock = Mock(return_value="result")
        expected = "mod_result"
        def after_meth(event):
            event.result = expected

        meth = Method(mock)
        meth.after += after_meth

        result = meth()

        self.assertEqual(expected, result)
        self.assertEqual(expected, meth.after.events[0].result)

    def test_Method_is_a_descriptor(self):
        self.assertTrue(hasattr(Method, '__get__'))

    def test_Method_return_self_when_there_is_no_instance(self):
        expected = Method(lambda: True)
        my_class = self.__get_class_with_method(expected)
        self.assertEqual(getattr(my_class, 'method'), expected)

    def test_Method_has_func_name_attr_from_passed_func(self):
        def a_func():
            pass
        method = Method(a_func)
        self.assertEqual(method.func_name, 'a_func')

    def test_Method_is_bound_to_instance_from_func_name_when_getting(self):
        def another_func():
            pass
        my_object = self.__get_object_with_func(another_func)
        self.assertNotIn('another_func', my_object.__dict__)
        getattr(my_object, 'method')
        self.assertIn('another_func', my_object.__dict__)

    def test_Method_events_are_differents_from_instance_method(self):
        func1 = Mock()
        func2 = Mock()
        call = Mock()
        my_object = self.__get_object_with_func(func1, nocall=func2)
        my_object.method.before += call
        my_object.method()
        my_object.nocall()
        call.assert_called_once_with(my_object.method.before.events[0])


### Helpers:

    def __get_class_with_method(self, method, **kwargs):
        kwargs['method'] = method
        return type('my_class', tuple(), kwargs)

    def __get_object_with_func(self, func, **kwargs):
        method = Method(func)
        for key, item in kwargs.items():
            kwargs[key] = Method(item)
        my_class = self.__get_class_with_method(method, **kwargs)
        return my_class()
