fiql_parser
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

To Install
----------

**From source (tar.gz or checkout)**

Unpack the archive, enter the fiql_parser directory and run:

    python setup.py install

Using fiql_parser
-----------------

Currently the functionality is pretty limited so there isn't a lot to say on
how to use it.

**Parsing a FIQL formatted string**

    from fiql_parser import parse_str_to_expression

    fiql_str = "last_name==foo*,(age=lt=55;age=gt=5)"
    expression = parse_str_to_expression(fiql_str)

    expression.to_python()

**Building an Expression**

    from fiql_parser import (Expression, Constraint, Operator)

    expression = Expression()
    expression.add_element(Constraint('last_name', '==', 'foo*'))
    expression.add_element(Operator(','))
    sub_expression = Expression()
    sub_expression.add_element(Constraint('age', '=lt=', '55'))
    sub_expression.add_element(Operator(';'))
    sub_expression.add_element(Constraint('age', '=gt=', '5'))
    expression.add_element(sub_expression)

    fiql_str = str(expression)

TODO
----

* Add more parser options.
* Add methods to facilitate using code to generate FIQL strings more
  easily.

