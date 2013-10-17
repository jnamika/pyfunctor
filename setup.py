# -*- coding:utf-8 -*-

from setuptools import setup

import sys
sys.path.append('src')
sys.path.append('src/tests')

from pyfunctor import __version__, __license__, __author__, __email__, __doc__

setup(
    name         = 'pyfunctor',
    version      = __version__,
    description  = 'A Functor library for Python',
    long_description = __doc__,
    author       = __author__,
    author_email = __email__,
    license      = __license__,
    url          = 'https://github.com/jnamika/pyfunctor',
    keywords     = 'functor lazy pipeline block',
    packages     = ['pyfunctor'],
    package_dir  = {'' : 'src'},
    test_suite   = 'test4pyfunctor',
    classifiers  = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: %s' % __license__,
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
