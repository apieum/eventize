# -*- coding: utf8 -*-
from .. import TestCase, Mock
from eventize.descriptors.handlerValue import Value
from eventize.descriptors import named, WrapCondition


class NewValue(Value):
    event_types = {
        'attr1': Mock(),
        'attr2': Mock()
    }
    def set_handlers(self):
        self.attr1 = Mock(**{'when.return_value':'expect3'})
        self.attr2 = Mock()

class DescriptorCls(named.Named):
    attr1 = Mock()
    attr2 = Mock()
    def when(self, condition):
        return 'expect1'

class OwnerCls(named.Named):
    attr1 = DescriptorCls(default=Mock(**{'when.return_value':'expect2'}))
    attr2 = Mock()

class HandlerValueTest(TestCase):
    original_Named_ValueType = named.Named.ValueType

    def setUp(self):
        named.Named.ValueType = NewValue

    def tearDown(self):
        named.Named.ValueType = self.original_Named_ValueType

    def test_it_finds_handlers_names_with_set_handlers_state_changes(self):
        value = NewValue(None, '', None)
        self.assertEqual(set(['attr1', 'attr2']), value.event_handlers)

    def test_When_returns_a_conditionnal_wrapper(self):
        value = Value(None, '', None)
        self.assertIsInstance(value.when(None), WrapCondition)


    def test_When_returns_a_Wrapper_with_all_Value_handlers_for_inst_class_and_desc(self):
        class OwnerCls(object):
            attr1 = DescriptorCls()
        wrapper = NewValue(OwnerCls(), 'attr1', '').when(None)

        self.assertTrue(hasattr(wrapper, 'attr1'))
        self.assertTrue(hasattr(wrapper, 'attr2'))
        self.assertTrue(hasattr(wrapper, 'attr1_class'))
        self.assertTrue(hasattr(wrapper, 'attr2_class'))
        self.assertTrue(hasattr(wrapper, 'attr1_descriptor'))
        self.assertTrue(hasattr(wrapper, 'attr2_descriptor'))


    def test_When_Wrapper_attrs_return_result_of_attrwhen(self):
        class Cls(object):
            attr1 = OwnerCls()

        obj = Cls()
        wrapper = Cls.attr1.get_value(obj).when(lambda *args:True)

        self.assertEqual(wrapper.attr1, 'expect3')
        self.assertEqual(wrapper.attr1_class, 'expect2')
        self.assertEqual(wrapper.attr1_descriptor, 'expect1')


