# -*- coding: utf8 -*-
import unittest
from mock import Mock
from sys import version as SYS_VERSION

class TestCase(unittest.TestCase):
    if SYS_VERSION < '3':
        assertRaisesRegex = unittest.TestCase.assertRaisesRegexp


__all__=['TestCase', 'SYS_VERSION', 'Mock']
