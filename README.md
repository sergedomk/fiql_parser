# FIQL Parser

A Python parser for the Feed Item Query Language (FIQL).

## What is FIQL?

From the FIQL draft
[ https://tools.ietf.org/html/draft-nottingham-atompub-fiql-00 ]:

> The Feed Item Query Language (FIQL, pronounced "fickle") is a simple
> but flexible, URI-friendly syntax for expressing filters across the
> entries in a syndicated feed.

## How does FIQL work?

A Feed Item Query string looks something like this:

    last_name==foo*,(age=lt=55;age=gt=5)

The above query string is looking for all records with `last_name` starting
with `"foo"` OR `age` less than `55` AND greater than `5`. The parentheses in
the query work the same as they do in any logical expression.

This code includes a modification to the rule defined for `comparison` to deal
with an inconsistency. The change fixes an issue where the string `"=="` was NOT
a valid `comparison` and thus made most of the examples in the FIQL draft
incorrect.

This code also includes a modification to the accepted arg chars to include
`":"`. This change fixes the issue where RFC-3339 complaint `DateTime` values
were NOT valid and thus, once again, making examples in the FIQL draft
inaccurate. Since `":"` is a valid character in an HTTP query `\*( pchar / "/" /
"?" )`, I opted to fix the issue by simply allowing the `":"` in addition to the
other arg chars.

The `comparison` rule in this code is `( ( "=" \*ALPHA ) / fiql-delim ) "="`. This
rule allows for a string with no `ALPHA` characters.

The `arg-char` rule in this code is `unreserved / pct-encoded / fiql-delim /
"=" / ":"`. This allows for `":"` in arguments (ex. `2015-08-27T10:30:00Z`).

## To Install

**From PyPi**

```bash
$ pip install fiql-parser
```

**From source (tar.gz or checkout)**

Unpack the archive, enter the fiql\_parser directory and run:

```bash
$ python setup.py install
```

## Using fiql\_parser

Currently the functionality is pretty limited so there isn't a lot to say on
how to use it.

### Parsing a FIQL formatted string

```python
from fiql_parser import parse_str_to_expression

fiql_str = "last_name==foo*,(age=lt=55;age=gt=5)"
expression = parse_str_to_expression(fiql_str)

# to_python()'s output changed with Version 0.11.
print expression.to_python()
# Output of above would be:
['OR',
    ('last_name', '==', 'foo*'),
    ['AND',
        ('age', '<', '55'),
        ('age', '>', '5'),
    ]
]
```

### Building an Expression

**Method One**

```python
from fiql_parser import (Expression, Constraint, Operator)

expression = Expression()
expression.add_element(Constraint('last_name', '==', 'foo*'))
expression.add_element(Operator(','))
sub_expression = Expression()
sub_expression.add_element(Constraint('age', '=lt=', '55'))
sub_expression.add_element(Operator(';'))
sub_expression.add_element(Constraint('age', '=gt=', '5'))
expression.add_element(sub_expression)

print str(expression)
# Output of above would be:
"last_name==foo*,(age=lt=55;age=gt=5)"
```

**Method Two (Changed in Version 0.11)**

```python
from fiql_parser import Constraint

expression = Constraint('last_name', '==', 'foo*').op_or(
        Constraint('age', '=lt=', '55').op_and(
                Constraint('age', '=gt=', '5')
            )
        )

fiql_str = str(expression)
# Output of above would be:
"last_name==foo*,(age=lt=55;age=gt=5)"
```

## CHANGES

**Version 0.12**

Release on August 27th, 2015

* Added pylint to tox.
* Added Python3.4 support.

**Version 0.11**

Released on August 27th, 2015

* Update documentation to reflect new structure.
* BREAKS COMPATIBILITY WITH VERSIONS <= 0.10.
  * Adopt prefix format over inline for internal structure, `to_python()`
    output, and fluent expression build method.
* Add missing `py_modules` required to actually end up with a working
  package.

**Version 0.10**

Released on December 18th, 2014

* Updated documentation for compatibility pypi and github.
* Fixed some stuff in setup.py pre upload to pypi.

**Version 0.9**

Released on December 3rd, 2014

* First public release.
