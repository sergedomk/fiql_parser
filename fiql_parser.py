# -*- coding: utf-8 -*-
"""
Parse an FIQL formatted string.

Copyright 2014, by Serge Domkowski

FIQL is defined in the following IETF draft:

https://tools.ietf.org/html/draft-nottingham-atompub-fiql-00

This code includes a modification to the rule defined for `comparison` to deal
with an inconsistency. The change fixes an issue where the string "==" was NOT
a valid `comparison` and thus made most of the examples in the FIQL draft
incorrect.

The `comparison` rule in this code is ( ( "=" *ALPHA ) / fiql-delim ) "=". This
rule allows for a string with no ALPHA characters.
"""
from __future__ import unicode_literals

import re
import urllib


#: Percent-encoding
PCT_ENCODING_REGEX = r'%[A-Fa-f0-9]{2}'

#: Unreserved Characters
UNRESERVED_REGEX = r'[A-Za-z0-9-\._~]'

#: FIQL delimiter
FIQL_DELIM_REGEX = r'[\!\$\'\*\+]'

#: Comparison operator (e.g., '=gt=')
COMPARISON_REGEX = r'(=[A-Za-z]*|' + FIQL_DELIM_REGEX + ')='

#: Selector - Identifies the portion of an entry that a constraint applies to.
SELECTOR_REGEX = '(' + UNRESERVED_REGEX + '|' + PCT_ENCODING_REGEX + ')+'

#: Arg-char - Characters allowed in an argument.
ARG_CHAR_REGEX = '(' + UNRESERVED_REGEX + '|' + PCT_ENCODING_REGEX + '|' + \
        FIQL_DELIM_REGEX + '|' + '=)'

#: Argument - Identifies the value that the comparison operator should use when
#: validating the constraint.
ARGUMENT_REGEX = ARG_CHAR_REGEX + '+'

#: A FIQL constraint - When processed yields a boolean value.
CONSTRAINT_REGEX = '(' + SELECTOR_REGEX + ')((' + COMPARISON_REGEX + ')' + \
        '(' + ARGUMENT_REGEX + '))?'

#: FIQL constraint regex (compiled).
CONSTRAINT_COMP = re.compile(CONSTRAINT_REGEX)

#: Mappings for common FIQL Comparisons.
COMPARISONS = {
    '==': '==',
    '!=': '!=',
    '=gt=': '>',
    '=ge=': '>=',
    '=lt=': '<',
    '=le=': '<=',
}

#: Mappings of FIQL operators to common terms.
OPERATOR_MAP = {
    ';': 'AND',
    ',': 'OR',
}


class FiqlException(Exception):
    """Exception class for FIQL parsing/retrieval errors."""
    pass


class Operator(object):

    """
    FIQL Operator.

    FIQL has two operators. ';' which is the logical `AND` and ',' for the
    logical `OR`.
    """
    #pylint: disable=too-few-public-methods

    def __init__(self, fiql_op_str):
        """Initialize instance of Operator.

        Args:
            fiql_op_str (string): The FIQL operator (e.g., ';').
        """
        try:
            self.value = OPERATOR_MAP[fiql_op_str]
        except KeyError:
            raise FiqlException(
                "'%s' is not a valid FIQL operator" % fiql_op_str)

    def __str__(self):
        """Return the Operator instance as a string."""
        return self.value


class FiqlBase(object):

    """
    FIQL Expression/Constraint base.
    """

    def __init__(self):
        """Initialize instance of FiqlBase."""
        self.parent = None

    def set_parent(self, parent):
        """Set parent Expression for this object.

        Args:
            parent (Expression): The Expression which contains this object.

        Raises:
            FiqlException: Parent must be of type Expression.
        """
        if not isinstance(parent, Expression):
            raise FiqlException("Parent must be of %s not %s" % (
                Expression, type(parent)))
        self.parent = parent

    def get_parent(self):
        """Get the parent Expression for this object.

        Returns:
            (Expression) The Expression which contains this object.

        Raises:
            FiqlException: Parent is None.
        """
        if not isinstance(self.parent, Expression):
            raise FiqlException("Parent must be of %s not %s" % (
                Expression, type(self.parent)))
        return self.parent


class Constraint(FiqlBase):

    """
    FIQL Constraint.

    The Constraint is the smallest logical unit for a FIQL Expression. It
    itself must evaluate to `True` or `False` and contains no smaller unit
    which itself can evaulate to `True` or `False`.
    """
    #pylint: disable=too-few-public-methods

    def __init__(self, selector, comparison=None, argument=None):
        """Initialize instance of Constraint.

        Args:
            selector (string): URL decoded constraint `selector`.
            comparison (string): Optional parsed/mapped `comparison`
                operator. Defaults to `None`.
            argument (string): Optional URL decoded constraint `argument`.
                Defaults to `None`.
        """
        super(Constraint, self).__init__()
        self.selector = selector
        self.comparison = comparison
        self.argument = argument

    def __str__(self):
        """Return the Constraint instance as a string."""
        if self.argument:
            return "{0} {1} {2}".format(self.selector, self.comparison,
                                        self.argument)
        return self.selector


class Expression(FiqlBase):

    """
    FIQL Expression.

    Both Constraint and Expression classes extend the FiqlBase class. This
    simplifies some parsing logic as most of the rules which apply to
    Constraints are equally applicable to Expressions.
    """

    def __init__(self):
        """Initialize instance of Expression."""
        super(Expression, self).__init__()
        self.elements = []

    def has_constraint(self):
        """Return whether or not this Expression has any Constraints (The
        first element must be either an Expression or a constraint).
        """
        return len(self.elements) and isinstance(self.elements[0], FiqlBase)

    def add_element(self, element):
        """Add an element to the Expression.

        The element may be a Constraint, Expression, or Operator. This method
        contains logic to ensure that the expression starts with a Constraint
        or Expression and that there is always an Operator between any two
        Expressions/Constraints.

        Args:
            element: Constraint, Expression, or Operator.

        Raises:
            FiqlException: Operator not proceeded by Constraint.
        """
        if not isinstance(element, FiqlBase):
            if not isinstance(element, Operator):
                raise FiqlException("%s is not a valid element type" % (
                    element.__class__))
            if not len(self.elements):
                raise FiqlException("%s proceeding initial %s" % (
                    element.__class__, Constraint))
            if not isinstance(self.elements[-1], FiqlBase):
                raise FiqlException("%s can not be followed by %s" % (
                    self.elements[-1].__class__, element.__class__))
        else:
            if len(self.elements) and \
                    isinstance(self.elements[-1], FiqlBase):
                raise FiqlException("%s can not be followed by %s" % (
                    self.elements[-1].__class__, element.__class__))
            element.set_parent(self)
        self.elements.append(element)

    def create_nested_expression(self):
        """Create a nested Expression, add it as an element to this Expression,
        and return it.

        Returns:
            (Expression): The newly created nested Expression.
        """
        sub = Expression()
        self.add_element(sub)
        return sub

    def __str__(self):
        """Return the Expression instance as a string."""
        elements_str = " ".join(["{0}".format(elem) for elem in self.elements])
        if self.parent:
            return "( " + elements_str + " )"
        return elements_str


def iter_parse(fiql_str):
    """Iterate through the FIQL string. Returns a tuple containing the
    following FIQL components:

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

    Returns:
        (tuple) Preamble, selector, comparison, argument.

    Raises:
        FiqlException: Unable to parse string due to incorrect formatting.
    """
    while len(fiql_str):
        constraint_match = CONSTRAINT_COMP.split(fiql_str, 1)
        if len(constraint_match) < 2:
            yield (constraint_match[0], None, None, None)
            break
        yield (
            constraint_match[0],
            urllib.unquote_plus(constraint_match[1]),
            constraint_match[4],
            urllib.unquote_plus(constraint_match[6]) \
                    if constraint_match[6] else None
        )
        fiql_str = constraint_match[8]

def parse_str_to_expression(fiql_str):
    """Parse a FIQL formatted string into an Expression.
    Args:
        fiql_str (string): The FIQL formatted string we want to parse.

    Returns:
        (Expression) An Expression object representing the parsed FIQL string.

    Raises:
        FiqlException: Unable to parse string due to incorrect formatting.
    """
    expression = Expression()
    current = expression
    for (preamble, selector, comparison, argument) in iter_parse(fiql_str):
        if preamble:
            for char in preamble:
                if char == '(':
                    current = current.create_nested_expression()
                elif char == ')':
                    current = current.get_parent()
                else:
                    current.add_element(Operator(char))
        if selector:
            current.add_element(Constraint(
                selector, COMPARISONS.get(comparison, comparison), argument))
    if current != expression:
        raise FiqlException(
            "At least one nested expression was not correctly closed")
    if not expression.has_constraint():
        raise FiqlException("Parsed string '%s' contained no constraint" % \
                fiql_str)
    return expression

