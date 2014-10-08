import os
__all__=['name', 'version', 'url', 'author', 'author_email', 'license', 'description', 'long_description', 'classifiers', 'packages']

name = 'eventize'
version='0.4.3'
url='http://www.python.org/pypi/' + name
author='Gregory Salvan'
author_email='apieum@gmail.com'
license='LGPL'
description='Add events to object methods and attributes'
doc_source = os.path.join(os.path.dirname(__file__), 'doc', 'source')
long_description=open(os.path.join(doc_source, 'readme.rst')).read()
classifiers=[
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Development Status :: 4 - Beta",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
packages=['eventize', 'eventize.api', 'eventize.events', 'eventize.descriptors', 'eventize.method', 'eventize.attribute', 'eventize.typing', 'eventize.modifiers']
