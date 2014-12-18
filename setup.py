#!/usr/bin/python

from setuptools import setup

with open('README.md') as fd:
    readme = fd.read()

with open('requirements-testing.txt') as fd:
    test_reqs = fd.readlines()
    tests_require = [line for line in test_reqs if not line.startswith('#')]

setup(
    name = 'fiql-parser',
    version = '0.9',
    description = 'FIQL Parser',
    long_description = readme,
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
