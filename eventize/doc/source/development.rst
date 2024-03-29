
===========
Development
===========

Contributions are greatly appreciated.

Please use `github <https://github.com/apieum/eventize>`_ (issue tracker, pull requests...) or contact me at apieum [at] gmail [dot] com

--------
Testing
--------
Tests are my specs so code (except refactorings) without tests won't probably be accepted.
If you want to contribute please add tests.

Test recommended requirements::

  pip install -r dev-requirements.txt


Sometimes --spec-color doesn't function.
You should uninstall nosecolor and nosespec then reinstall nosecolor and nosespec separatly (nosecolor first).

You can fix it like this::

  pip uninstall nosespec nosecolor
  pip install nosecolor && pip install nosespec


In order to have fast feedback with TDD loops, I develop with two virtualenvs (2.7 and 3.3 python versions) launched in a splited shell (tmux) which runs tests each time a file changes.
Use the code below with option --with-watch to launch tests this way.

Launching tests::

  git clone git@github.com:apieum/eventize.git
  cd eventize
  nosetests --with-spec --spec-color ./eventize
  # or with watch
  # nosetests --with-spec --spec-color --with-watch ./eventize


--------------
Documentation
--------------

Documentation is generated by sphinx from restructured text localized in doc/source. It is build by make (see doc/Makefile).

Except to explain implementation choices (why), **please avoid comments in code**. It aims at keeping focus on coding and avoiding outdated comments.
Keep long names (vars, functions, classes...) and explicit tests names (complete sentences) to have understandable code.

Building doc::

  git clone git@github.com:apieum/eventize.git
  cd eventize/eventize/doc
  make all  # or make *target* (see in Makefile for *target*)


----------------------
Continuous Integration
----------------------

CI is made by travis for different python versions (trying to maintain compatibility with v2 python).

It checks:
  * test suites (nosetest)
  * rst-lint this README
  * doc building
  * `code coverage <https://coveralls.io/github/apieum/eventize>`_


.. image:: https://api.travis-ci.com/apieum/eventize.svg?branch=master
    :target: https://app.travis-ci.com/github/apieum/eventize

.. image:: https://coveralls.io/repos/github/apieum/eventize/badge.svg?branch=master
    :target: https://coveralls.io/github/apieum/eventize?branch=master
