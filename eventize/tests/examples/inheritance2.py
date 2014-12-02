from eventize import Attribute

def titlecase(event):
    event.value = event.value.title()

class Name(Attribute):
    """nothing new"""

# when doing this:
Name.on_set.do(titlecase)
# all classes which use Attribute will have titlecase callback
assert titlecase in Attribute.on_set
# because without Subject:
assert Name.on_set is Attribute.on_set
