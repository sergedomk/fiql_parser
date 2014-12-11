# -*- coding: utf-8 -*-
"""
Tests against the classes representing FIQL query objects.
"""
from __future__ import unicode_literals

import unittest

from fiql_parser import (Operator, Constraint, Expression,
        FiqlException)


class TestObjects(unittest.TestCase):

    def test_operator_init(self):
        self.assertRaisesRegexp(FiqlException,
                "'i' is not a valid FIQL operator",
                Operator, 'i')

    def test_operator_to_string(self):
        sub_expression = Expression()
        sub_expression.add_element(Constraint('foo'))
        sub_expression.add_element(Operator(';'))
        sub_expression.add_element(Constraint('bar', '=gt=', '45'))
        expression = Expression()
        expression.add_element(Constraint('a', '==', 'wee'))
        expression.add_element(Operator(','))
        expression.add_element(sub_expression)
        expression.add_element(Operator(';'))
        expression.add_element(Constraint('key'))
        self.assertEqual("a==wee,(foo;bar=gt=45);key",
                str(expression))

    def test_operator_to_python(self):
        sub_expression = Expression()
        sub_expression.add_element(Constraint('foo'))
        sub_expression.add_element(Operator(';'))
        sub_expression.add_element(Constraint('bar', '=gt=', '45'))
        expression = Expression()
        expression.add_element(Constraint('a', '==', 'wee'))
        expression.add_element(Operator(','))
        expression.add_element(sub_expression)
        expression.add_element(Operator(';'))
        expression.add_element(Constraint('key'))
        self.assertEqual([
            ('a', '==', 'wee'), 'OR', [
                ('foo', None, None), 'AND', ('bar', '>', '45')
                ], 'AND', ('key', None, None)],
            expression.to_python())

    def test_constraint_init_with_defaults(self):
        constraint = Constraint('foo')
        self.assertEqual('foo', constraint.selector)
        self.assertIsNone(constraint.comparison)
        self.assertIsNone(constraint.argument)
        self.assertEqual('foo', str(constraint))

    def test_constraint_init(self):
        constraint = Constraint('foo', '==', 'bar')
        self.assertEqual('foo', constraint.selector)
        self.assertEqual('==', constraint.comparison)
        self.assertEqual('bar', constraint.argument)
        self.assertEqual('foo==bar', str(constraint))
        # invalid comparison
        self.assertRaisesRegexp(FiqlException,
                "'=gt' is not a valid FIQL comparison",
                Constraint, 'foo', '=gt', 'bar')

    def test_constraint_set_parent(self):
        constraint = Constraint('foo')
        another_constraint = Constraint('bar')
        self.assertRaisesRegexp(FiqlException,
                "Parent must be of <class 'fiql_parser.Expression'>" +
                " not <class 'fiql_parser.Constraint'>",
                constraint.set_parent, another_constraint)
        expression = Expression()
        constraint.set_parent(expression)
        self.assertEqual(expression, constraint.parent)

    def test_constraint_get_parent(self):
        constraint = Constraint('foo')
        self.assertRaisesRegexp(FiqlException,
                "Parent must be of <class 'fiql_parser.Expression'>" + \
                " not <type 'NoneType'>",
                constraint.get_parent)
        expression = Expression()
        constraint.set_parent(expression)
        self.assertEqual(expression, constraint.get_parent())

    def test_expression_has_constraint(self):
        expression = Expression()
        self.assertFalse(expression.has_constraint())
        expression.add_element(Constraint('foo'))
        self.assertTrue(expression.has_constraint())

    def test_expression_add_element(self):
        expression = Expression()
        self.assertRaisesRegexp(FiqlException,
                "<type 'unicode'> is not a valid element type",
                expression.add_element, 'foo')
        self.assertRaisesRegexp(FiqlException,
                "<class 'fiql_parser.Operator'> proceeding initial" + \
                " <class 'fiql_parser.Constraint'>",
                expression.add_element, Operator(';'))
        expression.add_element(Constraint('foo'))
        self.assertRaisesRegexp(FiqlException,
                "<class 'fiql_parser.Constraint'> can not be followed by" + \
                " <class 'fiql_parser.Constraint'>",
                expression.add_element, Constraint('bar'))
        expression.add_element(Operator(';'))
        self.assertRaisesRegexp(FiqlException,
                "<class 'fiql_parser.Operator'> can not be followed by" + \
                " <class 'fiql_parser.Operator'>",
                expression.add_element, Operator(','))
        expression.add_element(Constraint('bar'))
        self.assertEqual("foo;bar", str(expression))

    def test_expression_create_nested_expression(self):
        expression = Expression()
        sub_expression = expression.create_nested_expression()
        sub_sub_expression = sub_expression.create_nested_expression()
        self.assertEqual(expression, sub_expression.get_parent())
        self.assertEqual(sub_expression, sub_sub_expression.get_parent())
        self.assertRaisesRegexp(FiqlException,
                "<class 'fiql_parser.Expression'> can not be followed by" + \
                " <class 'fiql_parser.Expression'>",
                expression.create_nested_expression)
        expression = Expression()
        expression.add_element(Constraint('foo'))
        self.assertRaisesRegexp(FiqlException,
                "<class 'fiql_parser.Constraint'> can not be followed by" + \
                " <class 'fiql_parser.Expression'>",
                expression.create_nested_expression)

    def test_expression_get_parent(self):
        expression = Expression()
        self.assertRaisesRegexp(FiqlException,
                "Parent must be of <class 'fiql_parser.Expression'>" + \
                " not <type 'NoneType'>",
                expression.get_parent)
        sub_expression = expression.create_nested_expression()
        self.assertEqual(expression, sub_expression.get_parent())

    def test_expression_fluent(self):
        expression = Expression().constraint('foo', '==', 'bar') \
                .op_or() \
                .sub_expr(Expression() \
                        .constraint('age', '=lt=', '55') \
                        .op_and() \
                        .constraint('age', '=gt=', '5')
                    )
        self.assertEqual("foo==bar,(age=lt=55;age=gt=5)",
                str(expression))
        self.assertRaisesRegexp(FiqlException,
                "<class 'fiql_parser.Operator'> is not a valid Expression" + \
                " type.",
                Expression().sub_expr, Operator(';'))

    def test_constraint_fluent(self):
        expression = Constraint('foo', '==', 'bar').op_or() \
                .sub_expr(Constraint('age', '=lt=', '55') \
                        .op_and().constraint('age', '=gt=', '5')
                    )
        self.assertEqual("foo==bar,(age=lt=55;age=gt=5)",
                str(expression))

