# -*- coding: utf8 -*-
from .. import TestCase, Mock
from eventize.events import listen, Event, Handler

class Observer(object):
    pass

class ListenTest(TestCase):
    def test_it_set_an_attr_with_event_type_name_to_observer(self):
        observer = Observer()
        class ExpectedEvent(Event):
            pass
        listen(observer, ExpectedEvent)
        self.assertTrue(hasattr(observer, 'ExpectedEvent'))


    def test_set_attr_is_an_handler_by_default(self):
        observer = Observer()
        given = listen(observer, Event)
        self.assertIsInstance(given, Handler)

    def test_can_define_the_handler_with_third_argument(self):
        expected_handler = Handler()
        observer = Observer()
        listen(observer, Event, expected_handler)
        self.assertIs(observer.Event, expected_handler)

    def test_if_observer_already_listen_event_handler_of_same_type_it_is_not_replaced(self):
        observer = Observer()
        listen(observer, Event)
        handler = getattr(observer, 'Event')
        listen(observer, Event)
        self.assertIs(observer.Event, handler)

    def test_if_observer_already_listen_event_handler_of_different_type_it_is_replaced(self):
        class ExpectedHandler(Handler):
            pass
        expected = ExpectedHandler()
        observer = Observer()
        handler = listen(observer, Event)
        listen(observer, Event, expected)
        self.assertIsNot(observer.Event, handler)

    def test_when_replacing_handler_new_is_extended_by_old_values(self):
        class ExpectedHandler(Handler):
            pass
        handler = ExpectedHandler()
        expected = lambda event: event
        observer = Observer()
        listen(observer, Event, Handler(expected))
        given = listen(observer, Event, handler)
        self.assertIsInstance(given, ExpectedHandler)
        self.assertIn(expected, given)



