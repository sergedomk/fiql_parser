# -*- coding: utf-8 -*-
"""
FIQL Exceptions.
"""
from __future__ import unicode_literals
from __future__ import absolute_import


class FiqlException(Exception):
    """Base Exception class for FIQL errors."""
    pass

class FiqlObjectException(FiqlException):
    """Exception class for FIQL expression object errors."""
    pass

class FiqlFormatException(FiqlException):
    """Exception class for FIQL string parsing errors."""
    pass

