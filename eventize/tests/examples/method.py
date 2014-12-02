from eventize import before, after
from eventize.method import BeforeEvent, AfterEvent


class Observed(object):
    def __init__(self):
        self.valid = False

    def is_valid(self, *args):
        return self.valid

    def not_valid(self, event):
        assert event.name == "is_valid" # (event subject name)
        assert event.subject == self
        self.valid = not self.valid

class Logger(list):
    def log_before(self, event):
        assert type(event) is BeforeEvent
        self.append(self.message('before %s'  % event.name, *event.args, is_valid=event.subject.valid))

    def log_after(self, event):
        assert type(event) is AfterEvent
        self.append(self.message('after %s' % event.name, *event.args, is_valid=event.subject.valid))

    def message(self, event_name, *args, **kwargs):
        return "%s called with args: '%s', current:'%s'" % (event_name, args, kwargs['is_valid'])


args_have_permute = lambda event: 'permute' in event.args

my_object = Observed()
my_logs = Logger()

before_is_valid = before(my_object, 'is_valid')
before_is_valid += my_logs.log_before
before_is_valid.when(args_have_permute).do(my_object.not_valid)
after(my_object, 'is_valid').do(my_logs.log_after)

assert my_object.is_valid() is False
assert my_object.is_valid('permute') is True

assert my_logs == [
    my_logs.message('before is_valid', is_valid=False),
    my_logs.message('after is_valid', is_valid=False),
    my_logs.message('before is_valid', 'permute', is_valid=False),
    my_logs.message('after is_valid', 'permute', is_valid=True),
]
