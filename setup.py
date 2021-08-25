# -*- coding: utf8 -*-
from setuptools import setup
from eventize import metadata

setup(
    name=metadata.name,
    version=metadata.version,
    url=metadata.url,
    author=metadata.author,
    author_email=metadata.author_email,
    license=metadata.license,
    description=metadata.description,
    long_description=metadata.long_description,
    long_description_content_type='text/x-rst',
    classifiers=metadata.classifiers,
    packages=metadata.packages,
    include_package_data=True,
    zip_safe=True,
)

