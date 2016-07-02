# -*- coding: utf-8 -*-
"""
© Copyright 2014-2015, by Serge Domkowski.

.. note::

    This code includes a few modifications to rules in the FIQL draft.

    The rule defined for ``Comparison`` has been modifed to deal with an
    inconsistency in the draft documentation. The change fixes an issue where
    the string "==" was NOT a valid ``Comparison`` and thus made most of
    the examples in the FIQL draft incorrect.

    The accepted arg chars to have been modifed to include ":". This change
    fixes the issue where :rfc:`3339` compliant DateTime values were not valid
    unless the ":" was percent-encoded. This contradicted the FIQL draft
    ``date_str`` examples. Since ":" is a valid character in an HTTP query
    ``*( pchar / "/" / "?" )``, I opted to fix the issue by simply allowing
    the ":" in addition to the other arg chars.
"""
from __future__ import unicode_literals
from __future__ import absolute_import

__version__ = "0.15"

from .exceptions import FiqlException
from .exceptions import FiqlObjectException, FiqlFormatException
from .operator import Operator
from .constraint import Constraint
from .expression import Expression
from .parser import parse_str_to_expression

