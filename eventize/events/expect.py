# -*- coding: utf8 -*-
from inxpect import expect
from inxpect.expect.getters import AttrByName

class Expect(object):
    arg = expect.ListItem(AttrByName('args'))
    args = expect.List(AttrByName('args'))
    kwarg = expect.DictItem(AttrByName('kwargs'))
    kwargs = expect.Dict(AttrByName('kwargs'))
    subject = expect.ExpectSame(AttrByName('subject'))
    name = expect.Expect(AttrByName('name'))
    value = expect.Expect(AttrByName('value'))
    result = expect.Expect(AttrByName('result'))
    results = expect.List(AttrByName('results'))
    messages = expect.List(AttrByName('messages'))
