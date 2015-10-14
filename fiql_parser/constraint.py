# -*- coding: utf-8 -*-
"""
FIQL Constraint.

Attributes:
    COMPARISON_MAP (dict): Mappings for common FIQL comparisons.
"""
from __future__ import unicode_literals
from __future__ import absolute_import

try:
    #pylint: disable=no-name-in-module
    from urllib import quote_plus
except ImportError:
    #pylint: disable=import-error,no-name-in-module
    from urllib.parse import quote_plus

from .exceptions import FiqlObjectException
from .constants import COMPARISON_COMP
from .expression import BaseExpression, Expression


COMPARISON_MAP = {
    '==': '==',
    '!=': '!=',
    '=gt=': '>',
    '=ge=': '>=',
    '=lt=': '<',
    '=le=': '<=',
}


class Constraint(BaseExpression):

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

        Raises:
            FiqlObjectException: Not a valid FIQL comparison.
        """
        super(Constraint, self).__init__()
        self.selector = selector
        # Validate comparison format.
        if comparison and COMPARISON_COMP.match(comparison) is None:
            raise FiqlObjectException(
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

