# -*- coding: utf-8 -*-
"""
The FIQL ``Constraint`` is the building block of the FIQL ``Expression``. A
FIQL ``Constraint`` is, on it's own, a very simple ``Expression``.

The ``constraint`` module includes the code used for managing comparison
acceptance and representation of the FIQL ``Constraint``.

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


# Common FIQL comparisons.
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
    The ``Constraint`` is the smallest logical unit for a FIQL ``Expression``.
    It itself must evaluate to ``True`` or ``False`` and contains no smaller
    unit which itself can evaulate to ``True`` or ``False``.

    Attributes:
        selector (string): Constraint ``selector``.
        comparison (string): Constraint ``comparison`` operator.
        argument (string): Constraint ``argument``.
    """

    def __init__(self, selector, comparison=None, argument=None):
        """Initialize instance of ``Constraint``.

        Args:
            selector (string): URL decoded constraint ``selector``.
            comparison (string, optional): Parsed/mapped ``comparison``
                operator. Defaults to ``None``.
            argument (string, optional): URL decoded constraint ``argument``.
                Defaults to ``None``.

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
        """Create an ``Expression`` using this ``Constraint`` and the specified
        additional ``elements`` joined using an "AND" ``Operator``

        Args:
            *elements (BaseExpression): The ``Expression`` and/or
                ``Constraint`` elements which the "AND" ``Operator`` applies
                to in addition to this ``Constraint``.

        Returns:
            Expression: Newly created ``Expression`` including this
                ``Constraint``, the elements passed in, and the "AND"
                ``Operator``.
        """
        return Expression().op_and(self, *elements)

    def op_or(self, *elements):
        """Create an ``Expression`` using this ``Constraint`` and the specified
        additional ``elements`` joined using an "OR" ``Operator``

        Args:
            *elements (BaseExpression): The ``Expression`` and/or
                ``Constraint`` elements which the "OR" ``Operator`` applies
                to in addition to this ``Constraint``.

        Returns:
            Expression: Newly created ``Expression`` including this
                ``Constraint``, the elements passed in, and the "OR"
                ``Operator``.
        """
        return Expression().op_or(self, *elements)

    def to_python(self):
        """Deconstruct the ``Constraint`` instance to a tuple.

        Returns:
            tuple: The deconstructed ``Constraint``.
        """
        return (
            self.selector,
            COMPARISON_MAP.get(self.comparison, self.comparison),
            self.argument
        )

    def __str__(self):
        """Represent the ``Constraint`` instance as a string.

        Returns:
            string: The represented ``Constraint``.
        """
        if self.argument:
            return "{0}{1}{2}".format(quote_plus(self.selector),
                                      self.comparison,
                                      quote_plus(self.argument))
        return self.selector

