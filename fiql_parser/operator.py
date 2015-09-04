# -*- coding: utf-8 -*-
"""
FIQL Operator.

Attributes:
    OPERATOR_MAP (dict of tuple): Mappings of FIQL operators to common terms
        and their associated precedence.
"""
from __future__ import unicode_literals
from __future__ import absolute_import

from .exceptions import FiqlException


OPERATOR_MAP = {
    ';': ('AND', 2),
    ',': ('OR', 1),
}


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

