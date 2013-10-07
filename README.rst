********
Eventize
********

.. image:: https://pypip.in/v/eventize/badge.png
        :target: https://pypi.python.org/pypi/eventize


Add events to object methods and attributes.

Methods support events "before" and "after"
Attributes support events: "on_get", "on_set", "on_del"

Events can be triggered conditionaly within arguments or user condition.

---------------------------------------------------------------------

**Table of Contents**


.. contents::
    :local:
    :depth: 1
    :backlinks: none


=============
Installation
=============

Install it from pypi::

  pip install eventize

or from sources::

  git clone git@github.com:apieum/eventize.git
  cd eventize
  python setup.py install

=====
Usage
=====

-----------------------------
Example 1 - observe a method:
-----------------------------

.. code-block:: python

    from eventize import EventMethod
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



===========
Development
===========

Fell free to give feedback or improvements.

Launch test::

  git clone git@github.com:apieum/eventize.git
  cd eventize
  nosetests --with-spec --spec-color ./


.. image:: https://secure.travis-ci.org/apieum/eventize.png?branch=master
   :target: https://travis-ci.org/apieum/eventize
