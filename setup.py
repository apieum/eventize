# -*- coding: utf8 -*-
from setuptools import setup
import os

pkgName = 'eventize'
setup(
    name=pkgName,
    version='0.4.1',
    url='http://www.python.org/pypi/' + pkgName,
    author='Grégory Salvan',
    author_email='apieum@gmail.com',
    license='LGPL',
    description='Add events to object methods and attributes',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "inxpect",
    ],
    include_package_data=True,
    packages=['eventize', 'eventize.api', 'eventize.events', 'eventize.descriptors', 'eventize.method', 'eventize.attribute'],
    zip_safe=True,
)
