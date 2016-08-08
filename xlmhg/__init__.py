# from __future__ import (absolute_import, division,
#                         print_function, unicode_literals)
# from builtins import *

import pkg_resources
# import os

__version__ = pkg_resources.require('xlmhg')[0].version

#if 'READTHEDOCS' not in os.environ or \
#        os.environ['READTHEDOCS'] != 'True':
    # this is certainly weird, but allows us to import the xlmhg version
    # number from "docs/conf.py" without running into other problems
from .result import mHGResult
from .test import xlmhg_test, get_xlmhg_test_result, get_xlmhg_O1_bound

__all__ = ['mHGResult', 'xlmhg_test', 'get_xlmhg_test_result',
           'get_xlmhg_O1_bound']