#!/usr/bin/python
"""
FIQL Parser
"""
import io
from setuptools import setup

with io.open('requirements-testing.txt') as fd:
    test_reqs = fd.readlines()
    tests_require = [line for line in test_reqs if not line.startswith('#')]

with io.open('README.rst') as fd:
    long_desc = fd.read()

setup(
    name = 'fiql-parser',
    version = '0.13',
    description = 'Python parser for the Feed Item Query Language (FIQL).',
    long_description = long_desc,
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
