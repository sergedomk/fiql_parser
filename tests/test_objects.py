# -*- coding: utf-8 -*-
"""
Tests against the classes representing FIQL query objects.
"""
from __future__ import unicode_literals
from __future__ import absolute_import

import unittest

from fiql_parser import (Operator, Constraint, Expression,
        FiqlObjectException)


class TestObjects(unittest.TestCase):

    def test_operator_init(self):
        self.assertRaisesRegexp(FiqlObjectException,
                "'i' is not a valid FIQL operator",
                Operator, 'i')

    def test_operator_precedence(self):
        operator_and = Operator(';')
        operator_or = Operator(',')
        self.assertEqual(operator_and, Operator(';'))
        self.assertEqual(operator_or, Operator(','))
        self.assertNotEqual(operator_and, operator_or)
        self.assertGreater(operator_and, operator_or)
        self.assertLess(operator_or, operator_and)

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
        self.assertRaisesRegexp(FiqlObjectException,
                "'=gt' is not a valid FIQL comparison",
                Constraint, 'foo', '=gt', 'bar')

    def test_constraint_set_parent(self):
        constraint = Constraint('foo')
        another_constraint = Constraint('bar')
        self.assertRaisesRegexp(FiqlObjectException,
                "Parent must be of" +
                " <class 'fiql_parser.expression.Expression'>" +
                " not <class 'fiql_parser.constraint.Constraint'>",
                constraint.set_parent, another_constraint)
        expression = Expression()
        constraint.set_parent(expression)
        self.assertEqual(expression, constraint.parent)

    def test_constraint_get_parent(self):
        constraint = Constraint('foo')
        self.assertRaisesRegexp(FiqlObjectException,
                "Parent must be of" +
                " <class 'fiql_parser.expression.Expression'>" +
                " not {0}".format(type(None)),
                constraint.get_parent)
        expression = Expression()
        constraint.set_parent(expression)
        self.assertEqual(expression, constraint.get_parent())

    def test_expression_has_constraint(self):
        expression = Expression()
        self.assertFalse(expression.has_constraint())
        expression.add_element(Constraint('foo'))
        self.assertTrue(expression.has_constraint())

    def test_expression_add_operator(self):
        expression = Expression()
        self.assertRaisesRegexp(FiqlObjectException,
                "<class 'fiql_parser.constraint.Constraint'>" +
                " is not a valid element type",
                expression.add_operator, Constraint('foo'))
        expression.add_operator(Operator(';'))
        self.assertEqual(Operator(';'), expression.operator)
        new_expression = expression.add_operator(Operator(','))
        self.assertEqual(Operator(';'), expression.operator)
        self.assertNotEqual(expression, new_expression)
        self.assertEqual(Operator(','), new_expression.operator)

    def test_expression_add_element(self):
        expression = Expression()
        self.assertRaisesRegexp(FiqlObjectException,
                "{0} is not a valid element type".format(type("")),
                expression.add_element, 'foo')
        expression.add_element(Constraint('foo'))
        expression.add_element(Constraint('bar'))
        expression.add_element(Operator(';'))
        self.assertEqual("foo;bar", str(expression))
        new_expression = expression.add_operator(Operator(','))
        self.assertEqual(Operator(';'), expression.operator)
        self.assertNotEqual(expression, new_expression)
        self.assertEqual(Operator(','), new_expression.operator)
        new_expression.add_element(Constraint('baa'))
        self.assertEqual("foo;bar,baa", str(new_expression))

    def test_expression_create_nested_expression(self):
        expression = Expression()
        sub_expression = expression.create_nested_expression()
        sub_sub_expression = sub_expression.create_nested_expression()
        self.assertEqual(expression, sub_expression.get_parent())
        self.assertEqual(sub_expression, sub_sub_expression.get_parent())
        expression = Expression()
        expression.add_element(Constraint('foo'))
        sub_expression = expression.create_nested_expression()

    def test_expression_get_parent(self):
        expression = Expression()
        self.assertRaisesRegexp(FiqlObjectException,
                "Parent must be of" +
                " <class 'fiql_parser.expression.Expression'>" +
                " not {0}".format(type(None)),
                expression.get_parent)
        sub_expression = expression.create_nested_expression()
        self.assertEqual(expression, sub_expression.get_parent())

    def test_expression_fluent(self):
        expression = Expression().op_or(
                Constraint('foo', '==', 'bar'),
                Expression().op_and(
                        Constraint('age', '=lt=', '55'),
                        Constraint('age', '=gt=', '5')
                    )
                )
        self.assertEqual("foo==bar,age=lt=55;age=gt=5",
                str(expression))
        self.assertRaisesRegexp(FiqlObjectException,
                "{0} is not a valid element type".format(type('')),
                Expression().op_or, 'foo')

    def test_constraint_fluent(self):
        expression = Constraint('foo', '==', 'bar').op_or(
                Constraint('age', '=lt=', '55').op_and(
                        Constraint('age', '=gt=', '5')
                    )
                )
        self.assertEqual("foo==bar,age=lt=55;age=gt=5",
                str(expression))

    def test_to_string(self):
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
        self.assertEqual("a==wee,foo;bar=gt=45;key",
                str(expression))

    def test_to_python(self):
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
                'OR',
                ('a', '==', 'wee'),
                ['AND',
                    ['AND', ('foo', None, None), ('bar', '>', '45')],
                    ('key', None, None)
                ]
            ], expression.to_python())

    def test_expression_default_operator(self):
        expression = Expression()
        expression.add_element(Constraint('a', '==', 'wee'))
        expression.add_element(Constraint('bar', '=gt=', '45'))
        expression.add_element(Constraint('key'))
        self.assertEqual("a==wee;bar=gt=45;key",
                str(expression))
        self.assertEqual([
                'AND',
                ('a', '==', 'wee'),
                ('bar', '>', '45'),
                ('key', None, None)
            ], expression.to_python())

