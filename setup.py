# Copyright (c) 2015 Florian Wagner
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

import sys
import os

from setuptools import setup, find_packages, Extension
from codecs import open
from os import path

root = 'xlmhg'
description = 'XL-mHG: A Nonparametric Test For Enrichment in Ranked Binary Lists.'
version = '1.1rc2'

try:
	import numpy as np # numpy is required
except ImportError:
	print 'You must install NumPy before installing XL-mHG!'
	sys.exit(1)

try:
	from Cython.Distutils import build_ext
except ImportError:
	print 'You must install Cython before installing XL-mHG!'
	sys.exit(1)

here = path.abspath(path.dirname(__file__))

long_description = ''
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# extensions
ext_modules = []
ext_modules.append(Extension(root + '.' + 'xlmhg_cython', sources= [root + os.sep + 'xlmhg_cython.pyx'], include_dirs = [np.get_include()]))

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
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 2.7',
    ],

    keywords='statistics nonparametric enrichment test ranked binary lists',

    #packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    packages=['xlmhg'],

	# extensions
	ext_modules = ext_modules,
	cmdclass = {'build_ext': build_ext},

	#libraries = [],

    install_requires=['numpy','cython'],

	# development dependencies
    #extras_require={},

	# data
    #package_data={}

	# data outside package
    #data_files=[],

	# executable scripts
    entry_points={
        #'console_scripts': []
    },
)
