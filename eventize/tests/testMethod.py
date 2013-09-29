# -*- coding: utf8 -*-
import unittest
from mock import Mock
from eventize.method import Method

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

        mock.assert_called_once_with("arg", kwarg="kwarg")


    def test_method_call_returns_func_argument_result(self):
        expected_returns = "foo"
        mock = Mock(return_value=expected_returns)
        meth = Method(mock)
        self.assertEqual(expected_returns, meth())

    def test_callables_attached_to_on_event_are_called_with_args(self):
        mock = Mock()
        on_meth = Mock()
        meth = Method(mock)
        meth.on += on_meth

        meth("arg", kwarg="kwarg")

        on_meth.assert_called_once_with("arg", kwarg="kwarg")

    def test_callables_attached_to_before_event_are_called_with_args(self):
        mock = Mock()
        before_meth = Mock(return_value=([], {}))
        meth = Method(mock)
        meth.before += before_meth

        meth("arg", kwarg="kwarg")

        before_meth.assert_called_once_with("arg", kwarg="kwarg")

    def test_before_event_must_returns_args(self):
        mock = Mock()
        meth = Method(mock)
        expected = (("arg", ),{'kwarg':"kwarg"})
        result = meth.before("arg", kwarg="kwarg")

        self.assertEqual(expected, result)

    def test_before_event_can_modify_args(self):
        mock = Mock()
        expected = (("mod_arg", ),{'kwarg':"mod_kwarg"})
        meth = Method(mock)
        meth.before += Mock(return_value=expected)
        result = meth.before("arg", kwarg="kwarg")

        self.assertEqual(expected, result)

    def test_callables_attached_to_after_event_are_called_with_result(self):
        mock = Mock(return_value="result")
        after_meth = Mock()
        meth = Method(mock)
        meth.after += after_meth

        meth("arg", kwarg="kwarg")

        after_meth.assert_called_once_with("result")


    def test_after_event_can_modify_result(self):
        mock = Mock(return_value="result")
        expected = "mod_result"
        meth = Method(mock)
        meth.after += Mock(return_value=expected)

        result = meth()

        self.assertEqual(expected, result)

