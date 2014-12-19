FIQL Parser
===========

A Python parser for the Feed Item Query Language (FIQL).

What is FIQL?
-------------

From the FIQL draft
[ https://tools.ietf.org/html/draft-nottingham-atompub-fiql-00 ]:

> The Feed Item Query Language (FIQL, pronounced "fickle") is a simple
> but flexible, URI-friendly syntax for expressing filters across the
> entries in a syndicated feed.

How does FIQL work?
-------------------

A Feed Item Query string looks something like this:

    last_name==foo*,(age=lt=55;age=gt=5)

The above query string is looking for all records with `last_name` starting
with "foo" OR `age` less than 55 AND greater than 5. The paranthesis in
the query work the same as they do in any logical expression.

This code includes a modification to the rule defined for `comparison` to deal
with an inconsistency. The change fixes an issue where the string "==" was NOT
a valid `comparison` and thus made most of the examples in the FIQL draft
incorrect.

The `comparison` rule in this code is ( ( "=" \*ALPHA ) / fiql-delim ) "=". This
rule allows for a string with no ALPHA characters.

To Install
----------

**From PyPi**

    pip install fiql-parser

**From source (tar.gz or checkout)**

Unpack the archive, enter the fiql_parser directory and run:

    python setup.py install

Using fiql_parser
-----------------

Currently the functionality is pretty limited so there isn't a lot to say on
how to use it.

**Parsing a FIQL formatted string**

```python
from fiql_parser import parse_str_to_expression

fiql_str = "last_name==foo*,(age=lt=55;age=gt=5)"
expression = parse_str_to_expression(fiql_str)

expression.to_python()
```

**Building an Expression**


* Method One

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

# The following will be "last_name==foo*,(age=lt=55;age=gt=5)"
fiql_str = str(expression)
```

* Method Two

```python
from fiql_parser import Constraint

expression = Constraint('last_name', '==', 'foo*') \
        .op_or() \
        .sub_expr(
            Constraint('age', '=lt=', '55') \
                    .op_and() \
                    .constraint('age', '=gt=', '5')
        )

# The following will be "last_name==foo*,(age=lt=55;age=gt=5)"
fiql_str = str(expression)
```

TODO
----

* Add more parser options.

