# -*- coding: utf-8 -*-
"""
FIQL has two operators. ";" which is the logical ``AND`` and "," for the
logical ``OR`` where ``AND`` has a logical precedence which is higher than that
of ``OR``.

The ``operator`` module includes the code used for managing comparison operator
acceptance, precedence, and representation of the FIQL ``Operator``.

Attributes:
    OPERATOR_MAP (dict of tuple): Mappings of FIQL operators to common terms
        and their associated precedence.
"""
from __future__ import unicode_literals
from __future__ import absolute_import

from .exceptions import FiqlObjectException


OPERATOR_MAP = {
    ';': ('AND', 2),
    ',': ('OR', 1),
}


class Operator(object):

    """
    The comparison ``Operator`` is the representation of the FIQL comparison
    operator.

    Attributes:
        value (string): The FIQL operator.
    """
    #pylint: disable=too-few-public-methods

    def __init__(self, fiql_op_str):
        """Initialize instance of ``Operator``.

        Args:
            fiql_op_str (string): The FIQL operator (e.g., ";").

        Raises:
            FiqlObjectException: Invalid FIQL operator.
        """
        if not fiql_op_str in OPERATOR_MAP:
            raise FiqlObjectException(
                "'%s' is not a valid FIQL operator" % fiql_op_str)
        self.value = fiql_op_str

    def to_python(self):
        """Deconstruct the ``Operator`` instance to a string.

        Returns:
            string: The deconstructed ``Operator``.
        """
        return OPERATOR_MAP[self.value][0]

    def __str__(self):
        """Represent the ``Operator`` instance as a string.

        Returns:
            string: The represented ``Operator``.
        """
        return self.value

    def __cmp__(self, other):
        """Compare using operator precedence.

        Args:
            other (Operator): The ``Operator`` we are comparing precedence
                against.

        Returns:
            integer: ``1`` if greater than ``other``, ``-1`` if less than
            ``other``, and ``0`` if of equal precedence of ``other``.
        """
        prec_self = OPERATOR_MAP[self.value][1]
        prec_other = OPERATOR_MAP[other.value][1]
        if prec_self < prec_other:
            return -1
        if prec_self > prec_other:
            return 1
        return 0

    def __eq__(self, other):
        """Of equal precendence.

        Args:
            other (Operator): The ``Operator`` we are comparing precedence
                against.

        Returns:
            boolean: ``True`` if of equal precendence of ``other``.
        """
        return OPERATOR_MAP[self.value][1] == OPERATOR_MAP[other.value][1]

    def __lt__(self, other):
        """Of less than precedence.

        Args:
            other (Operator): The ``Operator`` we are comparing precedence
                against.

        Returns:
            boolean: ``True`` if of less than precendence of ``other``.
        """
        return OPERATOR_MAP[self.value][1] < OPERATOR_MAP[other.value][1]

