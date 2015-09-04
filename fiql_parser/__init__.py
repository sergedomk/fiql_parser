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

from .exceptions import FiqlException
from .operator import Operator
from .constraint import Constraint
from .expression import Expression
from .parser import parse_str_to_expression

