# -*- coding: utf-8 -*-
"""
Tests against the FIQL string parsing functions.
"""
from __future__ import unicode_literals

import unittest

from fiql_parser import (parse_str_to_expression,
        iter_parse, FiqlException)


class TestParse(unittest.TestCase):

    def test_iter_parse(self):
        fiql_str = 'a==23;(b=gt=4,(c=ge=5;c=lt=15))'
        self.assertEqual([
                ('', 'a', '==', '23'),
                (';(', 'b', '=gt=', '4'),
                (',(', 'c', '=ge=', '5'),
                (';', 'c', '=lt=', '15'),
                ('))', None, None, None),
            ], list(iter_parse(fiql_str)))

    def test_parse_str_to_expression(self):
        fiql_strings = [
            ("foo%24==bar%23+more",
                ('foo$', '==', 'bar# more')),
            ("foo=gt=bar",
                ('foo', '>', 'bar')),
            ("foo=le=bar",
                ('foo', '<=', 'bar')),
            ("foo!=bar",
                ('foo', '!=', 'bar')),
            ("foo",
                ('foo', None, None)),
            ("foo==bar;goo=gt=5",
                [('foo', '==', 'bar'), 'AND', ('goo', '>', '5')]),
            ("foo==bar,goo=lt=5",
                [('foo', '==', 'bar'), 'OR', ('goo', '<', '5')]),
            ("foo==bar,(goo=gt=5;goo=lt=10)",
                [('foo', '==', 'bar'), 'OR', [
                    ('goo', '>', '5'), 'AND', ('goo', '<', '10')]]),
            ("((foo))",
                ('foo', None, None)),
        ]
        for test_str, expected_py in fiql_strings:
            expression = parse_str_to_expression(test_str)
            self.assertEqual(test_str, str(expression))
            self.assertEqual(expected_py, expression.to_python())

    def test_parse_str_to_expression_failure(self):
        not_fiql_strings = [
            "foo=bar",
            "foo==",
            "foo=",
            ";;foo",
            "(foo)(bar)",
            "(foo==bar",
        ]
        for test_str in not_fiql_strings:
            try:
                parse_str_to_expression(test_str)
                self.fail("FiqlException not raised parsing '%s'" % test_str)
            except FiqlException:
                pass

