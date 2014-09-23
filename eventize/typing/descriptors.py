from abc import ABCMeta

class HandlerDescriptor(object):
    "Methods or Attributes handlers"


class MethodDescriptor(HandlerDescriptor):
    "Methods handlers"


class AttributeDescriptor(HandlerDescriptor):
    "Attributes handlers"

HandlerDescriptor = ABCMeta(str('HandlerDescriptor'), (HandlerDescriptor, ), {})
MethodDescriptor = ABCMeta(str('MethodDescriptor'), (MethodDescriptor, ), {})
AttributeDescriptor = ABCMeta(str('AttributeDescriptor'), (AttributeDescriptor, ), {})
