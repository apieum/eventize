# -*- coding: utf8 -*-
from . import TestCase, Mock
from eventize.method import Method
from eventize.events.event import Event

class MethodTest(TestCase):
    def test_Method_is_a_callable_object(self):
        self.assertTrue(callable(Method))

    def test_Method_take_an_argument(self):
        expected = "__init__.*argument"

        with self.assertRaisesRegex(TypeError, expected):
            Method()

    def test_Method_argument_must_be_callable(self):
        expected = '"arg" is not callable'
        with self.assertRaisesRegex(AttributeError, expected):
            Method("arg")

    def test_Method_argument_is_called_when_object_is_called(self):
        mock = Mock()
        meth = Method(mock)
        meth("arg", kwarg="kwarg")
        mock.assert_called_once_with(meth, "arg", kwarg="kwarg")


    def test_Method_call_returns_func_argument_result(self):
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
        self.assertEqual(method.__name__, 'a_func')

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
        my_object.method('method')
        my_object.nocall('nocall')
        call.assert_called_once_with(my_object.method.before.events[0])

    def test_define_func_properties_from_callable_object(self):
        class CallableObject(object):
            def __call__(arg, kwarg1='kwarg'):
                '''func doc'''
                return True

        my_object = CallableObject()
        method = Method(my_object)
        # __doc__, __name__, __defaults__, __code__
        self.assertEqual('func doc', method.__doc__)
        self.assertEqual('CallableObject%s' % id(my_object), method.__name__)
        self.assertEqual(('kwarg', ), method.__defaults__)
        self.assertEqual(my_object.__call__.__code__, method.__code__)

    def test_define_func_properties_from_function(self):
        def my_function(arg, kwarg1='kwarg'):
            '''func doc'''
            return True
        method = Method(my_function)
        self.assertEqual('func doc', method.__doc__)
        self.assertEqual('my_function', method.__name__)
        self.assertEqual(('kwarg', ), method.__defaults__)
        self.assertEqual(my_function.__code__, method.__code__)

    def test_define_func_properties_from_method(self):
        method = Method(self.my_method)
        self.assertEqual('func doc', method.__doc__)
        self.assertEqual('my_method', method.__name__)
        self.assertEqual(('kwarg', ), method.__defaults__)
        self.assertEqual(self.my_method.__code__, method.__code__)

    def test_define_func_properties_from_class_function(self):
        method = Method(MethodTest.my_method)
        self.assertEqual('func doc', method.__doc__)
        self.assertEqual('my_method', method.__name__)
        self.assertEqual(('kwarg', ), method.__defaults__)
        self.assertEqual(MethodTest.my_method.__code__, method.__code__)

    def test_define_func_properties_from_class_method(self):
        method = Method(self.my_class_method)
        self.assertEqual('func doc', method.__doc__)
        self.assertEqual('my_class_method', method.__name__)
        self.assertEqual(('kwarg', ), method.__defaults__)
        self.assertEqual(self.my_class_method.__code__, method.__code__)

    def test_define_func_properties_from_static_method(self):
        method = Method(self.my_static)
        self.assertEqual('func doc', method.__doc__)
        self.assertEqual('my_static', method.__name__)
        self.assertEqual(('kwarg', ), method.__defaults__)
        self.assertEqual(self.my_static.__code__, method.__code__)

    def test_define_func_properties_from_lambda(self):
        my_function = lambda arg, kwarg1='kwarg': True
        method = Method(my_function)
        self.assertEqual(None, method.__doc__)
        self.assertEqual('lambda%s' % id(my_function), method.__name__)
        self.assertEqual(('kwarg', ), method.__defaults__)
        self.assertEqual(my_function.__code__, method.__code__)

    def test_define_func_properties_from_builtin_function(self):
        method = Method(dir)
        self.assertEqual(dir.__doc__, method.__doc__)
        self.assertEqual('dir', method.__name__)
        self.assertEqual(None, method.__defaults__)
        self.assertEqual(None, method.__code__)

### Helpers:

    def __get_class_with_method(self, method, **kwargs):
        kwargs['method'] = method
        return type('my_class', tuple(), kwargs)

    def __get_object_with_func(self, func, **kwargs):
        for key, item in list(kwargs.items()):
            kwargs[key] = Method(item)
        my_class = self.__get_class_with_method(Method(func), **kwargs)
        return my_class()

    def my_method(self, arg, kwarg1='kwarg'):
        '''func doc'''
        return True

    @staticmethod
    def my_static(arg, kwarg1='kwarg'):
        '''func doc'''
        return True

    @classmethod
    def my_class_method(cls, arg, kwarg1='kwarg'):
        '''func doc'''
        return True

