# -*- coding: utf-8 -*-
"""
FIQL Constants.
"""
from __future__ import unicode_literals
from __future__ import absolute_import

import re


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

