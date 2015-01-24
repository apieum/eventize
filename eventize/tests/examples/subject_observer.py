from eventize.events import Handler
from eventize.typing import Modifier

def is_string(event):
    return isinstance(event.content, str)

def titlecase(event):
    event.content = event.content.title()

class WeirdVisitor(Modifier):
    def visit(self, handler):
        handler.prepend([self.save_default])

    def save_default(self, event):
        self.default = event.content

my_visitor = WeirdVisitor()
handler = Handler(titlecase, my_visitor, condition=is_string)

# An Handler is a callable list
assert isinstance(handler, list)
assert callable(handler)

# handler contains 2 callbacks:
assert len(handler) == 2
assert titlecase in handler
assert my_visitor.save_default in handler
# it remove titlecase
handler -= titlecase
assert titlecase not in handler
# it adds titlecase
handler += titlecase


# Create event with attribute content and trigger it
event1 = handler.notify(content="a string")

assert my_visitor.default == "a string"
assert event1.content == "A String"

# if event.content is not a string propagation is stopped
# these 2 lines are sames as notify
event2 = handler.make_event(content=1234)
handler(event2)

assert len(handler.events) == 2
assert handler.events == (event1, event2)
expected_message = "Condition '%s' for event 'Event' return False" % id(is_string)
assert event2.messages[0] == expected_message

# we remove all past events:
handler.clear_events()
assert len(handler.events) == 0

# we remove all callbacks and events:
handler.clear()
assert len(handler) == 0

is_a_name = lambda event: event.content == "a name"
# create a new subhandler with a condition:
handler.when(is_a_name).do(my_visitor.save_default).then(titlecase)
event1 = handler.notify(content="a name")
event2 = handler.notify(content="a string")
# only "a name" is titlecased
assert event1.content == "A Name"
assert event2.content == "a string"

# save_default is called only for event1:
assert my_visitor.default == "a name"
