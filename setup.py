#!/usr/bin/python
"""
FIQL Parser
===========

A Python parser for the Feed Item Query Language (FIQL).

What is FIQL?
-------------

From the FIQL draft
[ https://tools.ietf.org/html/draft-nottingham-atompub-fiql-00 ]:

    The Feed Item Query Language (FIQL, pronounced "fickle") is a simple
    but flexible, URI-friendly syntax for expressing filters across the
    entries in a syndicated feed.

To Install
----------

.. code:: bash

    $ pip install fiql-parser

Using fiql_parser
-----------------

For detailed documentation go to the GitHub site.
"""

from setuptools import setup

with open('requirements-testing.txt') as fd:
    test_reqs = fd.readlines()
    tests_require = [line for line in test_reqs if not line.startswith('#')]

setup(
    name = 'fiql-parser',
    version = '0.10',
    description = 'Python parser for the Feed Item Query Language (FIQL).',
    long_description = __doc__,
    author = 'Serge Domkowski',
    author_email = 'sergedomk@gmail.com',
    url = 'https://github.com/sergedomk/fiql_parser',
    license = 'BSD',
    include_package_data = True,
    install_requires = [],
    tests_require = tests_require,
    platforms = ['any'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
    ],
)
