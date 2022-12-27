# Copyright (c) 2015-2019 Florian Wagner
#
# This file is part of XL-mHG.

import sys
import os
from os import path
import io
from sys import platform

from setuptools import setup, find_packages, Extension
from wheel.bdist_wheel import bdist_wheel

here = path.abspath(path.dirname(__file__))
root = 'xlmhg'
description = 'XL-mHG: A Semiparametric Test for Enrichment'
version = '2.5.4'

long_description = ''
with io.open(path.join(here, 'README.rst'), encoding='UTF-8') as fh:
    long_description = fh.read()

ext_modules = []
cmdclass = {}

install_requires = [
    'plotly>=3',
    'pip>=19',
]

# do not require installation if built by ReadTheDocs
# (we mock these modules in docs/source/conf.py)
if 'READTHEDOCS' not in os.environ or \
        os.environ['READTHEDOCS'] != 'True':
    install_requires.extend([
        'cython>=0.25, <1',
        'numpy>=1.15, <2',
    ])
else:
    pass
    #install_requires.extend([
    #])


try:
    # this can fail if numpy or cython isn't installed yet
    import numpy as np
    from Cython.Distutils import build_ext
    from Cython.Compiler import Options as CythonOptions

except ImportError:
    pass

else:
    # tell setuptools to build the Cython extension

    # only enable Cython line tracing if we're installing in Travis-CI!
    macros = []
    try:
        if os.environ['TRAVIS'] == 'true' and os.environ['CI'] == 'true' \
                and os.environ['TRAVIS_OS_NAME'] == 'linux' \
                and 'TRAVIS_TEST_RESULT' not in os.environ:
            # note: linetracing is temporarily disabled
            # macros.append(('CYTHON_TRACE', '0'))
            # CythonOptions.directive_defaults['linetrace'] = False

            # only way of setting linetrace without cythonize?
            macros.append(('CYTHON_TRACE', '1'))
            #CythonOptions.directive_defaults['linetrace'] = True
            cython_defaults = CythonOptions.get_directive_defaults()
            cython_defaults['linetrace'] = True
            print('Warning: Enabling line tracing in cython extension.'
                  'This` will slow it down by a factor of 20 or so!')
    except (KeyError, ImportError):
        # KeyError if environment variable is not set,
        # ImportError if cython is not yet installed
        pass

    macros.append(('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION'))
    ext_modules.append(
        Extension(root + '.' + 'mhg_cython', [root + '/mhg_cython.pyx'],
                  include_dirs=[np.get_include()],
                  define_macros=macros))

    cmdclass['build_ext'] = build_ext


# do not require installation of extensions if built by ReadTheDocs
# (we mock these modules in docs/source/conf.py)
if 'READTHEDOCS' in os.environ and os.environ['READTHEDOCS'] == 'True':
    ext_modules = []  # disable Cython extension
    if 'build_ext' in cmdclass:
        del cmdclass['build_ext']


# fix version tag for mac
class CustomBdistWheel(bdist_wheel):
    # source: http://lepture.com/en/2014/python-on-a-hard-wheel
    def get_tag(self):
        tag = bdist_wheel.get_tag(self)
        # print('I\'m running!!! Tag is "%s"' % str(tag))
        if platform == 'darwin':
            repl = 'macosx_10_6_x86_64.macosx_10_9_x86_64.macosx_10_10_x86_64'
            if tag[2] in ['macosx_10_6_x86_64', 'macosx_10_7_x86_64']:
                tag = (tag[0], tag[1], repl)
        return tag


cmdclass['bdist_wheel'] = CustomBdistWheel

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

        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
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

    # tests_require=[],

    # development dependencies
    extras_require={
         'docs': [
             'sphinx>=1.4.5, <2',
             'sphinx-rtd-theme>=0.1.9',
             'sphinxcontrib-napoleon>=0.5.3',
             #'mock>=2.0.0, <3',
         ],
        'tests': [
            'pytest>=2.8.5, <6',
            'pytest-cov>=2.2.1, <3',
            'scipy>=1.1, <2',
        ],
    },

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
