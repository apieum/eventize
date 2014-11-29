===========
Development
===========

Your feedback, code review, improvements or bugs, and help to document is appreciated.
You can contact me by mail: apieum [at] gmail [dot] com

Test recommended requirements::

  pip install -r dev-requirements.txt

Sometimes --spec-color doesn't function. Uninstall nosespec and nosecolor then reinstall nosecolor and nosespec separatly in this order (nosecolor first).

Launch tests::

  git clone git@github.com:apieum/eventize.git
  cd eventize
  nosetests --with-spec --spec-color ./eventize
  # or with watch
  # nosetests --with-spec --spec-color --with-watch ./eventize



.. image:: https://secure.travis-ci.org/apieum/eventize.png?branch=master
   :target: https://travis-ci.org/apieum/eventize
