# -*- coding: utf8 -*-
import os
__all__=['name', 'version', 'url', 'author', 'author_email', 'license', 'description', 'long_description', 'classifiers', 'packages']

name = 'eventize'
category = 'Software Development :: Libraries :: Python Modules'
release = version = '0.4.4'
url = 'http://www.python.org/pypi/' + name
author = u'Grégory Salvan'
author_email ='apieum@gmail.com'
license ='LGPL'
copyright = u'(C)2014, %s' % author
long_description = description = 'Add events to object methods and attributes'
project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
source_root = os.path.join(project_root, name)
doc_source = os.path.join(source_root, 'doc', 'source')
readme_file = os.path.join(project_root, 'README.rst')
if os.path.exists(readme_file):
    long_description = open(readme_file).read()
classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Development Status :: 4 - Beta",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    "Operating System :: OS Independent",
    "Topic :: %s" % category,
]
packages = ['eventize', 'eventize.api', 'eventize.events', 'eventize.descriptors', 'eventize.method', 'eventize.attribute', 'eventize.typing', 'eventize.modifiers']




