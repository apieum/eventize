from .. import TestCase, Mock
from eventize.attribute.value import Value


class ValueTest(TestCase):
    def test_when_2_values_binded_on_change_avoid_recursive_loop(self):
        obj = Mock()
        expected = "test"
        value1 = Value(obj, 'value1', expected)
        value2 = Value(obj, 'value2', expected)
        value1.on_change+= lambda event: value2.set(event.returns())
        value2.on_change+= lambda event: value1.set(event.returns())
        value1.set("expected")
        self.assertEqual(value2.get(), "expected")



