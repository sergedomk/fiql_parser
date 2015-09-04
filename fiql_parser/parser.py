# -*- coding: utf-8 -*-
"""
FIQL Parser.
"""
from __future__ import unicode_literals
from __future__ import absolute_import

try:
    #pylint: disable=no-name-in-module
    from urllib import unquote_plus
except ImportError:
    #pylint: disable=import-error,no-name-in-module
    from urllib.parse import unquote_plus

from .constants import CONSTRAINT_COMP
from .exceptions import FiqlException
from .expression import BaseExpression, Expression
from .constraint import Constraint
from .operator import Operator


def iter_parse(fiql_str):
    """Iterate through the FIQL string. Yields a tuple containing the
    following FIQL components for each iteration:

    - preamble: Any operator or opening/closing paranthesis preceeding a
      constraint or at the very end of the FIQL string.
    - selector: The selector portion of a FIQL constraint or `None` if yielding
      the last portion of the string.
    - comparison: The comparison portion of a FIQL constraint or `None` if
      yielding the last portion of the string.
    - argument: The argument portion of a FIQL constraint or `None` if yielding
      the last portion of the string.

    For usage see `parse_str_to_expression`.

    Args:
        fiql_str (string): The FIQL formatted string we want to parse.

    Yields:
        tuple: Preamble, selector, comparison, argument.
    """
    while len(fiql_str):
        constraint_match = CONSTRAINT_COMP.split(fiql_str, 1)
        if len(constraint_match) < 2:
            yield (constraint_match[0], None, None, None)
            break
        yield (
            constraint_match[0],
            unquote_plus(constraint_match[1]),
            constraint_match[4],
            unquote_plus(constraint_match[6]) \
                    if constraint_match[6] else None
        )
        fiql_str = constraint_match[8]

def parse_str_to_expression(fiql_str):
    """Parse a FIQL formatted string into an Expression.
    Args:
        fiql_str (string): The FIQL formatted string we want to parse.

    Returns:
        Expression: An Expression object representing the parsed FIQL string.

    Raises:
        FiqlException: Unable to parse string due to incorrect formatting.

    Example:

        >>> expression = parse_str_to_expression("name==bar,dob=gt=1990-01-01")

    """
    #pylint: disable=too-many-branches
    nesting_lvl = 0
    last_element = None
    expression = Expression()
    for (preamble, selector, comparison, argument) in iter_parse(fiql_str):
        if preamble:
            for char in preamble:
                if char == '(':
                    if isinstance(last_element, BaseExpression):
                        raise FiqlException("%s can not be followed by %s" % (
                            last_element.__class__, Expression))
                    expression = expression.create_nested_expression()
                    nesting_lvl += 1
                elif char == ')':
                    expression = expression.get_parent()
                    last_element = expression
                    nesting_lvl -= 1
                else:
                    if not expression.has_constraint():
                        raise FiqlException("%s proceeding initial %s" % (
                            Operator, Constraint))
                    if isinstance(last_element, Operator):
                        raise FiqlException("%s can not be followed by %s" % (
                            Operator, Operator))
                    last_element = Operator(char)
                    expression = expression.add_operator(last_element)
        if selector:
            if isinstance(last_element, BaseExpression):
                raise FiqlException("%s can not be followed by %s" % (
                    last_element.__class__, Constraint))
            last_element = Constraint(selector, comparison, argument)
            expression.add_element(last_element)
    if nesting_lvl != 0:
        raise FiqlException(
            "At least one nested expression was not correctly closed")
    if not expression.has_constraint():
        raise FiqlException("Parsed string '%s' contained no constraint" % \
                fiql_str)
    return expression

