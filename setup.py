#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
FIQL Parser
"""

import io
import re
from setuptools import setup

with io.open('requirements-testing.txt') as fd:
    test_reqs = fd.readlines()
    tests_require = [line for line in test_reqs if not line.startswith('#')]

with io.open('README.rst') as fd:
    long_desc = fd.read()

# Caculate the version number.
with io.open('fiql_parser/__init__.py', encoding='utf-8') as fd:
    for line in fd:
        version_match = re.match("__version__ = ['\"]([^'\"]*)['\"]", line)
        if version_match:
            version = version_match.group(1)
            break
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name = 'fiql-parser',
    version = version,
    description = 'Python parser for the Feed Item Query Language (FIQL).',
    long_description = long_desc,
    author = 'Serge Domkowski',
    author_email = 'sergedomk@gmail.com',
    url = 'https://github.com/sergedomk/fiql_parser',
    license = 'BSD',
    include_package_data = True,
    packages=['fiql_parser'],
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
