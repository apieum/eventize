# -*- coding: utf8 -*-
from .. import TestCase, Mock
from eventize.method import Method

class MethodTest(TestCase):
    def setUp(self):
        Method.before.remove_all()
        Method.after.remove_all()

    def test_Method_is_a_descriptor(self):
        self.assertTrue(hasattr(Method, '__get__'))

    def test_Method_argument_must_be_callable(self):
        first_arg = 'string'
        expected = '"%s" is not callable' % first_arg
        class ClassWithMethod(object):
            method = Method(first_arg)
        obj = ClassWithMethod()

        with self.assertRaisesRegex(AttributeError, expected):
            obj.method()


    def test_Method_argument_is_called_when_object_is_called(self):
        mock = Mock()
        class ClassWithMethod(object):
            method = Method(mock)
        obj = ClassWithMethod()

        obj.method("arg", kwarg="kwarg")
        mock.assert_called_once_with(obj, "arg", kwarg="kwarg")


    def test_Method_call_returns_func_argument_result(self):
        expected_returns = "foo"
        mock = Mock(return_value=expected_returns)
        class ClassWithMethod(object):
            method = Method(mock)
        obj = ClassWithMethod()

        self.assertEqual(expected_returns, obj.method())

    def test_callables_attached_to_before_event_are_called_with_event(self):
        mock = Mock()
        on_meth = Mock()
        class ClassWithMethod(object):
            method = Method(mock)
        obj = ClassWithMethod()

        obj.method.before += on_meth

        obj.method("arg", kwarg="kwarg")
        on_meth.assert_called_once_with(obj.method.before.events[0])

    def test_before_event_can_modify_args(self):
        mock = Mock()
        expected_args = ["mod_arg"]
        expected_kwargs = {'kwargs':"mod_kwarg"}
        def before_meth(event):
            event.args = expected_args
            event.kwargs = expected_kwargs

        class ClassWithMethod(object):
            method = Method(mock)
        obj = ClassWithMethod()

        obj.method.before += before_meth
        obj.method("arg", kwarg="kwarg")

        mock.assert_called_once_with(obj, *expected_args, **expected_kwargs)

    def test_callables_attached_to_after_event_are_called_with_event(self):
        mock = Mock(return_value="result")
        after_meth = Mock()
        class ClassWithMethod(object):
            method = Method(mock)
        obj = ClassWithMethod()

        obj.method.after += after_meth
        obj.method("arg", kwarg="kwarg")

        after_meth.assert_called_once_with(obj.method.after.events[0])


    def test_after_event_can_modify_result(self):
        mock = Mock(return_value="result")
        expected = "mod_result"
        def after_meth(event):
            event.result = expected

        class ClassWithMethod(object):
            method = Method(mock)
        obj = ClassWithMethod()

        obj.method.after += after_meth

        result = obj.method()

        self.assertEqual(expected, result)
        self.assertEqual(expected, obj.method.after.events[0].result)


    def test_Method_is_bound_to_instance_from_attribute_name_when_getting(self):
        expected_name = 'my_method'
        def a_func(self):
            pass
        class WithMethod(object):
            my_method = Method(a_func)

        my_object = WithMethod()
        self.assertNotIn(expected_name, my_object.__dict__)
        getattr(my_object, expected_name)
        self.assertIn(expected_name, my_object.__dict__)

    def test_Method_name_is_set_when_calling(self):
        expected_name = 'my_method'
        def a_func(self):
            pass
        class WithMethod(object):
            my_method = Method(a_func)

        my_object = WithMethod()

        self.assertNotIn(expected_name, my_object.__dict__)
        my_object.my_method()
        self.assertIn(expected_name, my_object.__dict__)
        self.assertEqual(expected_name, my_object.my_method.__name__)

    def test_Method_events_are_differents_from_instance_method(self):
        func1 = Mock()
        func2 = Mock()
        call = Mock()
        my_object = self.__get_object_with_func(func1, nocall=func2)
        my_object.method.before += call
        my_object.method('method')
        my_object.nocall('nocall')
        call.assert_called_once_with(my_object.method.before.events[0])

    def test_Method_class_events_are_added_to_instance(self):
        expected = 'class method'
        call_instance = lambda event: self.assertEqual(expected, event.attr)
        call_class = lambda event: setattr(event, 'attr', expected)
        my_object = self.__get_object_with_func(Mock())

        my_object.method.before += call_instance
        type(my_object).method.before += call_class

        my_object.method(attr='method')

        self.assertEqual(expected, my_object.method.before.events[0].attr)
        self.assertEqual(expected, type(my_object).method.before.events[0].attr)

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

