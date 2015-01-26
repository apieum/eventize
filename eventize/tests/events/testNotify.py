# -*- coding: utf8 -*-
from .. import TestCase, Mock
from eventize.events import listen, notify, Event, Handler, on_notify_error

class Observer(object):
    pass

class NotifyTest(TestCase):
    def test_if_observer_has_channel_it_is_notified_of_event(self):
        callback = Mock()
        observer = Observer()
        listen(observer, 'Event', Handler(callback))
        expected_event = notify(observer, Event())
        callback.assert_called_once_with(expected_event)

    def test_if_observer_has_not_channel_it_notifies_on_notify_error(self):
        log_error = Mock()
        on_notify_error.do(log_error)
        observer = Observer()
        expected_event = Event()
        given_event = notify(observer, expected_event)
        self.assertIs(given_event, expected_event)
        log_error.assert_called_once_with(given_event)
        on_notify_error.clear()
