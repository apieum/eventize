# -*- coding: utf8 -*-
from . import TestCase
from eventize import EventMethod

class DocExamplesTest(TestCase):

    def test_example_Event_method_1(self):

        self_valid = lambda self, *args, **kwargs: self.valid
        def not_valid(event):
            event.instance.valid = not event.instance.valid

        class Observed(object):
            is_valid = EventMethod(self_valid)
            def __init__(self):
                self.valid = False
                self.logs=[]

            def log(self, event):
                self.logs.append(self.log_message(*event.args, is_valid=self.valid))

            def log_message(self, *args, **kwargs):
                return "Validity Checks with args: '%s', current:'%s'" % (args, kwargs['is_valid'])



        my_object = Observed()
        my_object.is_valid.before += my_object.log
        my_object.is_valid.before.called_with('permute').do(not_valid)
        my_object.is_valid.after += my_object.log

        assert my_object.is_valid() is False
        assert my_object.is_valid('permute') is True

        assert my_object.logs == [
            my_object.log_message(is_valid=False),
            my_object.log_message(is_valid=False),
            my_object.log_message('permute', is_valid=False),
            my_object.log_message('permute', is_valid=True),
        ]



