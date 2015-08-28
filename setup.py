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

Changes
-------

Version 0.12: Released on August 27th, 2015

* Added pylint to tox.
* Added Python3.4 support.

Version 0.11: Released on August 27th, 2015

* Update documentation to reflect new structure.
* BREAKS COMPATIBILITY WITH VERSIONS <= 0.10.
  * Adopt prefix format over inline for internal structure, `to_python()`
    output, and fluent expression build method.
* Add missing `py_modules` required to actually end up with a working
  package.

See GitHub site for changes prior the most recent release.

"""
import io
from setuptools import setup

with io.open('requirements-testing.txt') as fd:
    test_reqs = fd.readlines()
    tests_require = [line for line in test_reqs if not line.startswith('#')]

setup(
    name = 'fiql-parser',
    version = '0.12',
    description = 'Python parser for the Feed Item Query Language (FIQL).',
    long_description = __doc__,
    author = 'Serge Domkowski',
    author_email = 'sergedomk@gmail.com',
    url = 'https://github.com/sergedomk/fiql_parser',
    license = 'BSD',
    include_package_data = True,
    py_modules=['fiql_parser'],
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
    ],
)
