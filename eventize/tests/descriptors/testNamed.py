# -*- coding: utf8 -*-
from .. import TestCase, Mock
from eventize.descriptors import named, WrapCondition

class NamedValueTest(TestCase):
    def test_it_finds_handlers_names_with_set_handlers_state_changes(self):
        class NewValue(named.Value):
            def set_handlers(self):
                self.attr1 = None
                self.attr2 = None

        value = NewValue(None)
        self.assertEqual(set(['attr1', 'attr2']), value.event_handlers)

    def test_When_returns_a_conditionnal_wrapper(self):
        value = named.Value(None)
        self.assertIsInstance(value.when(None), WrapCondition)


    def test_When_returns_a_Wrapper_with_all_Value_handlers_for_inst_class_and_desc(self):
        class DescriptorCls(named.Named):
            attr1 = Mock()
            attr2 = Mock()

        class OwnerCls(object):
            attr1 = Mock()
            attr2 = Mock()
            desc = DescriptorCls()

        class NewValue(named.Value):
            def set_handlers(self):
                self.attr1 = Mock()
                self.attr2 = Mock()
        wrapper = NewValue(None, OwnerCls(), 'desc').when(None)

        self.assertTrue(hasattr(wrapper, 'attr1'))
        self.assertTrue(hasattr(wrapper, 'attr2'))
        self.assertTrue(hasattr(wrapper, 'attr1_class'))
        self.assertTrue(hasattr(wrapper, 'attr2_class'))
        self.assertTrue(hasattr(wrapper, 'attr1_descriptor'))
        self.assertTrue(hasattr(wrapper, 'attr2_descriptor'))



    def test_When_Wrapper_attrs_return_result_of_attrwhen(self):
        class NewValue(named.Value):
            def set_handlers(self):
                self.attr1 = Mock(**{'when.return_value':'expect3'})

        class DescriptorCls(named.Named):
            ValueType = NewValue
            def when(self, condition):
                return 'expect1'

        class OwnerCls(named.Named):
            ValueType = NewValue
            attr1 = DescriptorCls(Mock(**{'when.return_value':'expect2'}))

        class Cls(object):
            attr1 = OwnerCls()

        obj = Cls()
        wrapper = Cls.attr1.get_value(obj).when(lambda *args:True)

        self.assertEqual(wrapper.attr1, 'expect3')
        self.assertEqual(wrapper.attr1_class, 'expect2')
        self.assertEqual(wrapper.attr1_descriptor, 'expect1')



