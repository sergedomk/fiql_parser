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

Unpack the archive, enter the sphinxcontrib-examplecode directory and run:

    python setup.py install

Using fiql_parser
-----------------

TODO

