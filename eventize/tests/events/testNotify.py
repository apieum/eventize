# -*- coding: utf8 -*-
from .. import TestCase, Mock
from eventize.events import listen, notify, Event, Handler

class Observer(object):
    pass

class NotifyTest(TestCase):
    def test_if_observer_has_channel_it_is_notified_of_event(self):
        callback = Mock()
        observer = Observer()
        listen(observer, Event, Handler(callback))
        expected_event = notify(observer, Event())
        callback.assert_called_once_with(expected_event)

    def test_if_observer_has_not_channel_nothing_happens(self):
        observer = Observer()
        expected_event = Event()
        given_event = notify(observer, expected_event)
        self.assertIs(given_event, expected_event)
