# -*- coding: utf8 -*-
from eventize.tests import TestCase, Mock
from eventize.events.conditions import Conditions, expect
from eventize.events.event import Event


class ConditionsTest(TestCase):
    def test_it_apply_to_an_event(self):
        conditions = Conditions()
        with self.assertRaisesRegex(TypeError, 'Event'):
            conditions(object())

    def test_it_should_call_each_callback_it_contains_until_false(self):
        callback1 = Mock(return_value=True)
        callback2 = Mock(return_value=False)
        callback3 = Mock(return_value=True)
        conditions = Conditions(callback1, callback2, callback3)
        event = Event(self)

        self.assertFalse(conditions(event))
        callback1.assert_called_once_with(event)
        callback2.assert_called_once_with(event)
        self.assertEqual(callback3.call_count, 0)

class expectedTest(TestCase):
    def test_arg_returns_true_if_event_contains_arg(self):
        event = Event(self, 'arg')
        self.assertTrue(expect.arg('arg') in event)

    def test_args_returns_true_if_event_contains_all_arg(self):
        event = Event(self, 'arg1', 'arg2')
        self.assertTrue(expect.args('arg1', 'arg2') in event)

    def test_kwarg_returns_true_if_event_contains_kwarg_with_right_value(self):
        event = Event(self, kwarg='kwarg')
        self.assertTrue(expect.kwarg('kwarg', 'kwarg') in event)

    def test_kwargs_returns_true_if_event_contains_all_kwargs_with_rights_values(self):
        event = Event(self, kwarg1='kwarg1', kwarg2=2)
        self.assertTrue(expect.kwargs(kwarg1='kwarg1', kwarg2=2) in event)

    def test_subject_returns_true_if_event_contains_same_object(self):
        event = Event(self, kwarg1='kwarg1', kwarg2=2)
        self.assertTrue(expect.subject(self) in event)

    def test_result_returns_true_if_event_result_is_equal(self):
        event = Event(self)
        event.result = 'result'
        self.assertTrue(expect.result('result') in event)

    def test_result_type_returns_true_if_event_result_type_is_the_same(self):
        event = Event(self)
        event.result = False
        self.assertTrue(expect.result.type_is(type(True)) in event)

    def test_name_instance_of_returns_true_if_event_name_is_instance(self):
        event = Event(self, name="name")
        self.assertTrue(expect.name.instance_of(type('')) in event)

    def test_value_instance_of_returns_false_if_event_value_is_not_instance(self):
        event = Event(self, value="value")
        self.assertFalse(expect.value.instance_of((Mock, type(None))) in event)

    def test_name_returns_true_if_event_kwarg_is_equal(self):
        event = Event(self, name='name')
        self.assertTrue(expect.name('name') in event)

    def test_value_returns_true_if_event_value_is_equal(self):
        event = Event(self, value='value')
        self.assertTrue(expect.value('value') in event)

    def test_can_create_a_new_property_with_other_getter(self):
        getter = lambda this, default=None: getattr(this, 'args', default)[0]
        arg1 = expect.arg.new(getter)
        event = Event(self, 'value')
        self.assertTrue(arg1('value') in event)

    def test_can_expect_value_of_an_arg_at_given_index(self):
        event = Event(self, 'arg1', 'arg2')
        self.assertTrue('arg2' == expect.arg.at(1) in event)

    def test_can_expect_value_of_a_kwarg_at_given_key(self):
        event = Event(self, kwarg1='value1', kwarg2='value2')
        self.assertTrue('value2' == expect.kwarg.at('kwarg2') in event)

    def test_can_expect_instance_of_a_kwarg_at_given_key(self):
        event = Event(self, kwarg1='value1', kwarg2='value2')
        self.assertTrue(expect.kwarg.at('kwarg2').instance_of(type('')) in event)

    def test_can_chain_expectations(self):
        event = Event(self, 'arg1', 'arg2', 'arg3')
        event.result = True
        self.assertTrue(expect.arg.at(0).equal_to('arg1') & expect.arg('arg2') & expect.result(True) in event)
        self.assertTrue(expect.arg.at(0).equal_to('arg') | expect.arg('arg2') | expect.result(False) in event)
        self.assertTrue(expect.arg.at(0).equal_to('arg') | expect.arg('arg2') & expect.result(True) in event)
