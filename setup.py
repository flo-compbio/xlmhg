# Copyright (c) 2015, 2016 Florian Wagner
#
# This file is part of XL-mHG.
#
# XL-mHG is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License, Version 3,
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import sys
import os
from os import path
import io
from sys import platform

from setuptools import setup, find_packages, Extension

try:
    import numpy as np  # numpy is required upfront
except ImportError:
    print('You must install NumPy before installing XL-mHG! '
          'Try `pip install numpy`.')
    sys.exit(1)

try:
    from Cython.Distutils import build_ext  # Cython is required upfront
except ImportError:
    print('You must installCython before installing XL-mHG! '
          'Try `pip install cython`.')
    sys.exit(1)

from Cython.Distutils import build_ext
from Cython.Compiler import Options as CythonOptions
import numpy as np

root = 'xlmhg'
description = 'XL-mHG: A Semiparametric Test for Enrichment'
version = '2.2.5'

install_requires = [
    'future >= 0.15.2, < 1',
    'six >= 1.10.0, < 2',
    'cython >= 0.23.4, < 1',
    'numpy >= 1.8, < 2',
]

cmdclass = {}
ext_modules = []

# do not require installation of extension if built by ReadTheDocs
# (we mock these modules in docs/source/conf.py)
if 'READTHEDOCS' not in os.environ or \
        os.environ['READTHEDOCS'] != 'True':

    # tell setuptools to build the Cython extension
    cmdclass['build_ext'] = build_ext

    # only enable Cython line tracing if we're installing in Travis-CI!
    macros = []
    try:
        if os.environ['TRAVIS'] == 'true' and os.environ['CI'] == 'true' \
                and 'TRAVIS_TEST_RESULT' not in os.environ:
            # note: linetracing is temporarily disabled
            # macros.append(('CYTHON_TRACE', '0'))
            # CythonOptions.directive_defaults['linetrace'] = False

            # only way of setting linetrace without cythonize?
            macros.append(('CYTHON_TRACE', '1'))
            CythonOptions.directive_defaults['linetrace'] = True
            print('Warning: Enabling line tracing in cython extension.'
                  'This will slow it down by a factor of 20 or so!')
    except KeyError:
        pass

    ext_modules.append(
        Extension(root+'.'+'mhg_cython', [root + '/mhg_cython.pyx'],
                  include_dirs=[np.get_include()],
                  define_macros=macros)
    )


here = path.abspath(path.dirname(__file__))

long_description = ''
with io.open(path.join(here, 'README.rst'), encoding='UTF-8') as fh:
    long_description = fh.read()

# extensions
setup(
    name='xlmhg',

    version=version,

    description=description,
    long_description=long_description,

    url='https://github.com/flo-compbio/xlmhg',

    author='Florian Wagner',
    author_email='florian.wagner@duke.edu',

    license='GPLv3',

    # see https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Cython',
    ],

    keywords=('statistics nonparametric semiparametric enrichment test '
              'ranked lists'),

    # packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    packages=find_packages(exclude=['docs', 'tests*']),

    # extensions
    ext_modules=ext_modules,
    cmdclass=cmdclass,

    # libraries = [],

    install_requires=install_requires,

    tests_require=[
        'pytest >= 2.8.5, < 3',
        'pytest-cov >= 2.2.1, < 3',
        'scipy >= 0.17.0',
    ],

    # development dependencies
    # extras_require={},

    # data
    package_data={
        'xlmhg': ['xlmhg/mhg_cython.pyx',
                  'tests/*',
                  'README.rst', 'LICENSE', 'CHANGELOG.rst'],
    },

    # data outside package
    # data_files=[],

    # executable scripts
    entry_points={
        # 'console_scripts': []
    },
)
