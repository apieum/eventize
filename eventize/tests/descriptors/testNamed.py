# -*- coding: utf8 -*-
from .. import TestCase, Mock
from eventize.descriptors import named

class NamedValueTest(TestCase):
    def test_finds_handlers_names_with_set_handlers_state_changes(self):
        class NewValue(named.Value):
            def set_handlers(self):
                self.attr1 = None
                self.attr2 = None

        value = NewValue(None)
        self.assertEqual(set(['attr1', 'attr2']), value.event_handlers)

