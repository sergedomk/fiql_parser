# -*- coding: utf-8 -*-
"""
Tests against the FIQL regex structures.
"""
from __future__ import unicode_literals
from __future__ import absolute_import

import re
import unittest

from fiql_parser.constants import (
    PCT_ENCODING_REGEX, UNRESERVED_REGEX,
    FIQL_DELIM_REGEX, COMPARISON_REGEX, SELECTOR_REGEX,
    ARG_CHAR_REGEX, ARGUMENT_REGEX, CONSTRAINT_REGEX)


class TestRegex(unittest.TestCase):

    def test_pct_encoding(self):
        re_comp = re.compile(PCT_ENCODING_REGEX + '$')
        self.assertIsNotNone(re_comp.match("%5E"))
        self.assertIsNotNone(re_comp.match("%AF"))
        self.assertIsNotNone(re_comp.match("%02"))
        self.assertIsNotNone(re_comp.match("%C4"))
        self.assertIsNotNone(re_comp.match("%ad"))
        self.assertIsNotNone(re_comp.match("%2b"))
        self.assertIsNotNone(re_comp.match("%f1"))
        self.assertIsNone(re_comp.match("###"))
        self.assertIsNone(re_comp.match("%A"))
        self.assertIsNone(re_comp.match("%G1"))
        self.assertIsNone(re_comp.match("%AAA"))

    def test_unreserved(self):
        re_comp = re.compile(UNRESERVED_REGEX + r'+$')
        self.assertIsNotNone(re_comp.match("POIUYTREWQASDFGHJKLMNBVCXZ"))
        self.assertIsNotNone(re_comp.match("qwertyuioplkjhgfdsazxcvbnm"))
        self.assertIsNotNone(re_comp.match("1234567890._-~"))
        # Fail if we get even one reserved char
        self.assertIsNone(re_comp.match(':'))
        self.assertIsNone(re_comp.match('/'))
        self.assertIsNone(re_comp.match('?'))
        self.assertIsNone(re_comp.match('#'))
        self.assertIsNone(re_comp.match('['))
        self.assertIsNone(re_comp.match(']'))
        self.assertIsNone(re_comp.match('@'))
        self.assertIsNone(re_comp.match('!'))
        self.assertIsNone(re_comp.match('$'))
        self.assertIsNone(re_comp.match('&'))
        self.assertIsNone(re_comp.match("'"))
        self.assertIsNone(re_comp.match('('))
        self.assertIsNone(re_comp.match(')'))
        self.assertIsNone(re_comp.match('*'))
        self.assertIsNone(re_comp.match(','))
        self.assertIsNone(re_comp.match(';'))
        self.assertIsNone(re_comp.match('='))

    def test_fiql_delim(self):
        re_comp = re.compile(FIQL_DELIM_REGEX + r'+$')
        self.assertIsNotNone(re_comp.match("!$'*+"))
        self.assertIsNone(re_comp.match('='))

    def test_comparison(self):
        re_comp = re.compile(COMPARISON_REGEX + '$')
        self.assertIsNotNone(re_comp.match("=gt="))
        self.assertIsNotNone(re_comp.match("=ge="))
        self.assertIsNotNone(re_comp.match("=lt="))
        self.assertIsNotNone(re_comp.match("=le="))
        self.assertIsNotNone(re_comp.match("!="))
        self.assertIsNotNone(re_comp.match("$="))
        self.assertIsNotNone(re_comp.match("'="))
        self.assertIsNotNone(re_comp.match("*="))
        self.assertIsNotNone(re_comp.match("+="))
        # This test should fail per spec but that didn't make sense.
        self.assertIsNotNone(re_comp.match("=="))
        self.assertIsNone(re_comp.match("="))
        self.assertIsNone(re_comp.match("=gt"))
        self.assertIsNone(re_comp.match("=01="))

    def test_selector(self):
        re_comp = re.compile(SELECTOR_REGEX + '$')
        self.assertIsNotNone(re_comp.match("ABC%3Edef_34%04"))
        self.assertIsNone(re_comp.match('#'))
        self.assertIsNone(re_comp.match('!'))
        self.assertIsNone(re_comp.match('='))
        self.assertIsNone(re_comp.match(''))

    def test_argument(self):
        re_comp = re.compile(ARGUMENT_REGEX + '$')
        self.assertIsNotNone(re_comp.match("ABC%3Edef_34~.-%04!$'*+:="))
        self.assertIsNone(re_comp.match('?'))
        self.assertIsNone(re_comp.match('&'))
        self.assertIsNone(re_comp.match(','))
        self.assertIsNone(re_comp.match(';'))
        self.assertIsNone(re_comp.match(''))

    def test_constraint(self):
        re_comp = re.compile(CONSTRAINT_REGEX)
        self.assertEqual(['', 'foo', 'o', '==bar', '==', '=', 'bar', 'r', ''],
                re_comp.split("foo==bar", 1))
        self.assertEqual(['', 'foo', 'o', '=gt=bar', '=gt=', '=gt', 'bar', 'r', ''],
                re_comp.split("foo=gt=bar", 1))
        self.assertEqual(['', 'foo', 'o', '=le=bar', '=le=', '=le', 'bar', 'r', ''],
                re_comp.split("foo=le=bar", 1))
        self.assertEqual(['', 'foo', 'o', '!=bar', '!=', '!', 'bar', 'r', ''],
                re_comp.split("foo!=bar", 1))
        self.assertEqual(['', 'foo', 'o', None, None, None, None, None, '=bar'],
                re_comp.split("foo=bar", 1))
        self.assertEqual(['', 'foo', 'o', None, None, None, None, None, '=='],
                re_comp.split("foo==", 1))
        self.assertEqual(['', 'foo', 'o', None, None, None, None, None, '='],
                re_comp.split("foo=", 1))
        self.assertEqual(['', 'foo', 'o', None, None, None, None, None, ''],
                re_comp.split("foo", 1))

