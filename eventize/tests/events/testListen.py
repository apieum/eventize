# -*- coding: utf8 -*-
from .. import TestCase, Mock
from eventize.events import stop_listen, listen, Handler

class Observer(object):
    pass

class ListenTest(TestCase):
    def setUp(self):
        if hasattr(Observer, '__listen__'):
            delattr(Observer, '__listen__')

    def test_it_set_an_attr_with_channel_to_observer(self):
        observer = Observer()
        listen(observer, 'expected channel')
        self.assertTrue(hasattr(observer, '__listen__'))
        self.assertIn('expected channel', getattr(observer, '__listen__'))

    def test_setted_attr_is_an_Handler_by_default(self):
        observer = Observer()
        given = listen(observer, 'channel')
        self.assertIsInstance(given, Handler)

    def test_can_define_the_handler_with_third_argument(self):
        expected_handler = Handler()
        observer = Observer()
        given = listen(observer, 'channel', expected_handler)
        self.assertIs(given, expected_handler)

    def test_if_observer_already__listen_event_handler_and_none_given_it_is_not_replaced_(self):
        observer = Observer()
        handler = listen(observer, 'channel')
        given = listen(observer, 'channel')
        self.assertIs(given, handler)

    def test_if_observer_already__listen_event_handler_and_one_given_it_is_replaced_(self):
        class ExpectedHandler(Handler):
            pass
        expected = ExpectedHandler()
        observer = Observer()
        handler = listen(observer, 'channel')
        given = listen(observer, 'channel', expected)
        self.assertIsNot(given, handler)

    def test_when_replacing_handler_new_is_extended_by_old_values(self):
        class ExpectedHandler(Handler):
            pass
        handler = ExpectedHandler()
        expected = lambda event: event
        observer = Observer()
        listen(observer, 'channel', Handler(expected))
        given = listen(observer, 'channel', handler)
        self.assertIsInstance(given, ExpectedHandler)
        self.assertIn(expected, given)

    def test_when_listen_a_class_objects_changes_not_changes_class(self):
        handler = listen(Observer, 'channel')
        observer = Observer()
        self.assertIs(listen(Observer, 'channel'), listen(observer, 'channel'))
        callback = lambda event: event
        expected_handler = Handler(callback)
        listen(observer, 'channel', expected_handler)
        self.assertNotIn(callback, listen(Observer, 'channel'))
        self.assertIn(callback, listen(observer, 'channel'))

    def test_when_listen_a_class_class_changes_not_changes_objects(self):
        callback1 = lambda event: event
        callback2 = lambda event: event
        expected = lambda event: event
        observer = Observer()
        listen(Observer, 'channel', Handler(callback1))
        object_handler = listen(observer, 'channel', Handler(callback2)).do(expected)
        class_handler = listen(Observer, 'channel')
        object_handler = listen(observer, 'channel')
        self.assertIn(callback1, class_handler)
        self.assertNotIn(callback2, class_handler)
        self.assertNotIn(expected, class_handler)
        self.assertIn(callback1, object_handler)
        self.assertIn(callback2, object_handler)
        self.assertIn(expected, object_handler)


class StopListenTest(TestCase):
    def test_it_removes_handler_from_god_chapel(self):
        """god's mysterious ways ^^"""
        god = Observer()
        handler = listen(god, 'chapel')
        god_chapel = stop_listen(god, 'chapel')
        self.assertIs(handler, god_chapel)
        self.assertNotIn('chapel', god.__listen__)
