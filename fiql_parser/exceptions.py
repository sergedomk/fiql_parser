# -*- coding: utf-8 -*-
"""
The code in this package is intended to be used in one of two ways; Building
the object representation of a FIQL expression directly, or building the
object representation of a FIQL expression by parsing it from a FIQL string.

The ``Exception`` classes contained in this module are intended to
provide the flexibility to differentiate between errors resulting from
attempting to construct the expression object and those resulting from
incorrectly formatted FIQL strings.
"""
#pylint: disable=unnecessary-pass


from __future__ import unicode_literals
from __future__ import absolute_import


class FiqlException(Exception):
    """Base Exception class for FIQL errors."""
    pass


class FiqlObjectException(FiqlException):
    """Exception class for FIQL expression object errors."""
    pass


class FiqlParserException(FiqlException):
    """Exception class for FIQL input parsing errors."""
    pass


class FiqlFormatException(FiqlParserException):
    """Exception class for FIQL string parsing errors."""
    pass
