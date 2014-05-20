# -*- coding: utf8 -*-
from .. import descriptors
from .handler import Handler, Subject, InstanceHandler

@Subject
class Descriptor(descriptors.Named):
    on_get = Handler()
    on_set = Handler()
    on_del = Handler()

    def on_get_instance(self, instance):
        return self.get_value(instance).on_get

    def on_set_instance(self, instance):
        return self.get_value(instance).on_set

    def on_del_instance(self, instance):
        return self.get_value(instance).on_del

    def get_value(self, instance, default=None):
        return self.get(instance, self.get_alias(instance), default)

    def get(self, instance, alias, default=None):
        if self.is_not_set(instance, alias):
            return StoreValue(default)
        return instance.__dict__[alias]


    def set(self, instance, alias, value):
        event = self.on_set.trigger(instance, name=alias, value=value)
        self.on_set_instance(instance)(event)
        if alias not in instance.__dict__:
            instance.__dict__[alias] = StoreValue(event.value)
        else:
            instance.__dict__[alias].data = event.value


    def get_result(self, instance, alias, value):
        event = self.on_get.trigger(instance, name=alias, value=value.data)
        value.on_get(event)
        return event.returns()

    def delete(self, instance, alias):
        event = self.on_del.trigger(instance, name=alias)
        self.on_del_instance(instance)(event)
        delattr(instance.__dict__[alias], 'data')


class StoreValue(object):
    def __init__(self, value):
        self.on_get = InstanceHandler()
        self.on_set = InstanceHandler()
        self.on_del = InstanceHandler()
        self.data = value
