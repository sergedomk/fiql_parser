# -*- coding: utf-8 -*-
"""
Parse an FIQL formatted string.

Copyright 2014-2015, by Serge Domkowski

FIQL is defined in the following IETF draft:

https://tools.ietf.org/html/draft-nottingham-atompub-fiql-00

This code includes a modification to the rule defined for `comparison` to deal
with an inconsistency. The change fixes an issue where the string "==" was NOT
a valid `comparison` and thus made most of the examples in the FIQL draft
incorrect.

This code also includes a modification to the accepted arg chars to include
":". This change fixes the issue where RFC-3339 complaint DateTime values
were not valid and thus, once again, making examples in the FIQL draft
inaccurate. Since ":" is a valid character in an HTTP query *( pchar / "/" /
"?" ), I opted to fix the issue by simply allowing the ":" in addition to the
other arg chars.

The `comparison` rule in this code is ( ( "=" *ALPHA ) / fiql-delim ) "=". This
rule allows for a string with no ALPHA characters.

The `arg-char` rule in this code is unreserved / pct-encoded / fiql-delim /
"=" / ":". This allows for ":" in arguments.
"""
from __future__ import unicode_literals
from __future__ import absolute_import

import re
try:
    #pylint: disable=no-name-in-module
    from urllib import quote_plus, unquote_plus
except ImportError:
    #pylint: disable=import-error,no-name-in-module
    from urllib.parse import quote_plus, unquote_plus


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
        FIQL_DELIM_REGEX + '|' + '=|:)'

#: Argument - Identifies the value that the comparison operator should use when
#: validating the constraint.
ARGUMENT_REGEX = ARG_CHAR_REGEX + '+'

#: A FIQL constraint - When processed yields a boolean value.
CONSTRAINT_REGEX = '(' + SELECTOR_REGEX + ')((' + COMPARISON_REGEX + ')' + \
        '(' + ARGUMENT_REGEX + '))?'

#: FIQL constraint regex (compiled).
CONSTRAINT_COMP = re.compile(CONSTRAINT_REGEX)

#: FIQL comparison full string regex (compiled).
COMPARISON_COMP = re.compile(r'^' + COMPARISON_REGEX + r'$')

#: Mappings for common FIQL Comparisons.
COMPARISON_MAP = {
    '==': '==',
    '!=': '!=',
    '=gt=': '>',
    '=ge=': '>=',
    '=lt=': '<',
    '=le=': '<=',
}

#: Mappings of FIQL operators to common terms.
OPERATOR_MAP = {
    ';': ('AND', 2),
    ',': ('OR', 1),
}


class FiqlException(Exception):
    """Exception class for FIQL parsing/retrieval errors."""
    pass


class Operator(object):

    """
    FIQL Operator.

    FIQL has two operators. ';' which is the logical `AND` and ',' for the
    logical `OR`.

    Attributes:
        value (string): The FIQL operator.
    """
    #pylint: disable=too-few-public-methods

    def __init__(self, fiql_op_str):
        """Initialize instance of Operator.

        Args:
            fiql_op_str (string): The FIQL operator (e.g., ';').
        """
        if not fiql_op_str in OPERATOR_MAP:
            raise FiqlException(
                "'%s' is not a valid FIQL operator" % fiql_op_str)
        self.value = fiql_op_str

    def to_python(self):
        """Return the Operator instance as a string."""
        return OPERATOR_MAP[self.value][0]

    def __str__(self):
        """Return the Operator instance as a string."""
        return self.value

    def __cmp__(self, other):
        """Compare using operator precedence."""
        prec_self = OPERATOR_MAP[self.value][1]
        prec_other = OPERATOR_MAP[other.value][1]
        if prec_self < prec_other:
            return -1
        if prec_self > prec_other:
            return 1
        return 0

    def __eq__(self, other):
        """Of equal precendence."""
        return OPERATOR_MAP[self.value][1] == OPERATOR_MAP[other.value][1]

    def __lt__(self, other):
        """Of less than precedence."""
        return OPERATOR_MAP[self.value][1] < OPERATOR_MAP[other.value][1]


class FiqlBase(object):

    """
    FIQL Expression/Constraint base.

    Attributes:
        parent (Expression): The `Expression` which contains this object.
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
            Expression: The Expression which contains this object.

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

    Attributes:
        selector (string): Constraint `selector`.
        comparison (string): Constraint `comparison` operator.
        argument (string): Constraint `argument`.
    """

    def __init__(self, selector, comparison=None, argument=None):
        """Initialize instance of Constraint.

        Args:
            selector (string): URL decoded constraint `selector`.
            comparison (string, optional): Parsed/mapped `comparison`
                operator. Defaults to `None`.
            argument (string, optional): URL decoded constraint `argument`.
                Defaults to `None`.
        """
        super(Constraint, self).__init__()
        self.selector = selector
        # Validate comparison format.
        if comparison and COMPARISON_COMP.match(comparison) is None:
            raise FiqlException(
                "'%s' is not a valid FIQL comparison" % comparison)
        self.comparison = comparison
        self.argument = argument

    def op_and(self, *elements):
        """Add an 'AND' operator to a newly created Expression containing this
        Constraint and return the Expression.

        Args:
            *elements (Expressions and/or Constraints): The elements which this
                operator applies to.

        Returns:
            Expression: Newly created expression including this Constraint
                and the 'AND' operator.
        """
        return Expression().op_and(self, *elements)

    def op_or(self, *elements):
        """Add an 'OR' operator to a newly created Expression containing this
        Constraint and return the Expression.

        Args:
            *elements (Expressions and/or Constraints): The elements which this
                operator applies to.

        Returns:
            Expression: Newly created expression including this Constraint
                and the 'AND' operator.
        """
        return Expression().op_or(self, *elements)

    def to_python(self):
        """Return the Constraint instance as a tuple."""
        return (
            self.selector,
            COMPARISON_MAP.get(self.comparison, self.comparison),
            self.argument
        )

    def __str__(self):
        """Return the Constraint instance as a string."""
        if self.argument:
            return "{0}{1}{2}".format(quote_plus(self.selector),
                                      self.comparison,
                                      quote_plus(self.argument))
        return self.selector


class Expression(FiqlBase):

    """
    FIQL Expression.

    Both Constraint and Expression classes extend the FiqlBase class. This
    simplifies some parsing logic as most of the rules which apply to
    Constraints are equally applicable to Expressions.

    Attributes:
        elements (list): List of elements in this expression.
        operator (Operator): The operator which relates the elements in this
            expression.
    """

    def __init__(self):
        """Initialize instance of Expression."""
        super(Expression, self).__init__()
        self.elements = []
        self.operator = None
        # Keep track of which nested fragment we are in.
        self._working_fragment = self
        # Keep track of what was last added.
        self._last_element = None

    def has_constraint(self):
        """Return whether or not the working Expression has any Constraints."""
        return len(self.elements)

    def add_operator(self, operator):
        """Add an operator to the Expression.

        The Operator may result in a new expression if an operator already
        exists and is of a different precedence.

        There are three possibilities when adding an operator to an expression
        depending on whether or not an operator already exists.

          - No operator on the working expression; Simply set the operator and
            return self.
          - Operator already exists and is higher in precedence; The operator
            and last Constraint belong in a subexpression of the working
            expression.
          - Operator already exists and is lower in precedence; The operator
            belongs to the parent of the working expression whether one
            currently exists or not. To remain in the context of the top
            Expression, this method will return the parent here rather than
            self.

        Args:
            operator (Operator): What we are adding.

        Returns:
            Expression: self or related expression.

        Raises:
            FiqlExpression: operator is not a valid Operator.
        """
        if not isinstance(operator, Operator):
            raise FiqlException("%s is not a valid element type" % (
                operator.__class__))

        if not self._working_fragment.operator:
            self._working_fragment.operator = operator
        elif operator > self._working_fragment.operator:
            last_constraint = self._working_fragment.elements.pop()
            self._working_fragment = self._working_fragment \
                    .create_nested_expression()
            self._working_fragment.add_element(last_constraint)
            self._working_fragment.add_operator(operator)
        elif operator < self._working_fragment.operator:
            if self._working_fragment.parent:
                return self._working_fragment.parent.add_operator(operator)
            else:
                return Expression().add_element(self._working_fragment) \
                        .add_operator(operator)
        return self

    def add_element(self, element):
        """Add an element to the Expression.

        The element may be a Constraint, Expression, or Operator. This method
        contains logic to ensure that the expression starts with a Constraint
        or Expression and that there is always an Operator between any two
        Expressions/Constraints.

        Args:
            element: Constraint, Expression, or Operator.

        Returns:
            Expression: self

        Raises:
            FiqlException: element is not a valid type.
        """
        if isinstance(element, FiqlBase):
            element.set_parent(self._working_fragment)
            self._working_fragment.elements.append(element)
            return self
        else:
            return self.add_operator(element)

    def create_nested_expression(self):
        """Create a nested Expression, add it as an element to this Expression,
        and return it.

        Returns:
            Expression: The newly created nested Expression.
        """
        sub = Expression()
        self.add_element(sub)
        return sub

    def op_and(self, *elements):
        """Fluently add an 'AND' operator to the expression.

        Args:
            *elements (Expressions and/or Constraints): The elements which this
                operator applies to.

        Returns:
            Expression: self
        """
        expression = self.add_operator(Operator(';'))
        for element in elements:
            expression.add_element(element)
        return expression

    def op_or(self, *elements):
        """Fluently add an 'OR' operator to the expression.

        Args:
            *elements (Expressions and/or Constraints): The elements which this
                operator applies to.

        Returns:
            Expression: self
        """
        expression = self.add_operator(Operator(','))
        for element in elements:
            expression.add_element(element)
        return expression

    def to_python(self):
        """Return the Expression instance as list of tuples or tuple (If a
        single constraint).
        """
        if len(self.elements) == 0:
            return None
        if len(self.elements) == 1:
            return self.elements[0].to_python()
        operator = self.operator or Operator(';')
        return [operator.to_python()] + \
            [elem.to_python() for elem in self.elements]

    def __str__(self):
        """Return the Expression instance as a string."""
        operator = self.operator or Operator(';')
        elements_str = str(operator).join(
            ["{0}".format(elem) for elem in self.elements])
        if self.parent:
            parent_operator = self.parent.operator or Operator(';')
            if parent_operator > operator:
                return "(" + elements_str + ")"
        return elements_str


def iter_parse(fiql_str):
    """Iterate through the FIQL string. Returns a tuple containing the
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

    Returns:
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
                    if isinstance(last_element, FiqlBase):
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
            if isinstance(last_element, FiqlBase):
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

