# -*- coding: utf-8 -*-
"""
Compiled and uncompiled regular expressions representing the various syntax
rules used in the FIQL specification.

.. _FIQL Draft#section-3.2:
    https://tools.ietf.org/html/draft-nottingham-atompub-fiql-00#section-3.2

Attributes:
    PCT_ENCODING_REGEX: Regular expression representing Percent-Encoding
        (:rfc:`3986#section-2.1`).
    UNRESERVED_REGEX: Regular expression repesenting Unreserved Characters
        (:rfc:`3986#section-2.3`).
    FIQL_DELIM_REGEX: Regular expression representing the FIQL Delimiter
        (`FIQL Draft#section-3.2`_).
    COMPARISON_REGEX: Regular expression representing the FIQL Comparison
        operator; e.g., "=gt=" (`FIQL Draft#section-3.2`_). This rule includes
        a modification to the rule in the FIQL draft that correctly allows for
        a string with no ALPHA characters.
    SELECTOR_REGEX: Regular expression representing the FIQL Selector
        (`FIQL Draft#section-3.2`_). The Selector identifies the portion of an
        entry that a Constraint applies to.
    ARG_CHAR_REGEX: Regular expression representing the characters allowed in
        a FIQL Argument (`FIQL Draft#section-3.2`_). This rule includes a
        modification to the rule in the FIQL draft that allows for ":" in
        arguments (Example: "2015-08-27T10:30:00Z").
    ARGUMENT_REGEX: Regular expression represeting the FIQL Argument
        (`FIQL Draft#section-3.2`_). The Argument identifies the value that the
        Comparison operator should use when validating the Constraint.
    CONSTRAINT_REGEX: Regular expression representing the FIQL Constraint
        (`FIQL Draft#section-3.2`_). The Constraint, when processed, yields a
        ``boolean`` value.
    CONSTRAINT_COMP: Compiled version of ``CONSTRAINT_REGEX``.
    COMPARISON_COMP: Compiled version of ``CONSTRAINT_REGEX`` as a full string.
"""
from __future__ import unicode_literals
from __future__ import absolute_import

import re


# Percent-encoding
PCT_ENCODING_REGEX = r'%[A-Fa-f0-9]{2}'

# Unreserved Characters
UNRESERVED_REGEX = r'[A-Za-z0-9-\._~]'

# FIQL delimiter
FIQL_DELIM_REGEX = r'[\!\$\'\*\+]'

# Comparison operator
COMPARISON_REGEX = r'(=[A-Za-z]*|' + FIQL_DELIM_REGEX + ')='

# Selector
SELECTOR_REGEX = '(' + UNRESERVED_REGEX + '|' + PCT_ENCODING_REGEX + ')+'

# Arg-char
ARG_CHAR_REGEX = '(' + UNRESERVED_REGEX + '|' + PCT_ENCODING_REGEX + '|' + \
        FIQL_DELIM_REGEX + '|' + '=|:)'

# Argument
ARGUMENT_REGEX = ARG_CHAR_REGEX + '+'

# Constraint
CONSTRAINT_REGEX = '(' + SELECTOR_REGEX + ')((' + COMPARISON_REGEX + ')' + \
        '(' + ARGUMENT_REGEX + '))?'

# Constraint (compiled)
CONSTRAINT_COMP = re.compile(CONSTRAINT_REGEX)

# Comparison; full string (compiled)
COMPARISON_COMP = re.compile(r'^' + COMPARISON_REGEX + r'$')

