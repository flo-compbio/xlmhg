# from __future__ import (absolute_import, division,
#                         print_function, unicode_literals)
# from builtins import *

import pkg_resources

__version__ = pkg_resources.require('xlmhg')[0].version

from .result import mHGResult
from .test import xlmhg_test, get_xlmhg_test_result, get_xlmhg_O1_bound

__all__ = ['mHGResult', 'xlmhg_test', 'get_xlmhg_test_result',
           'get_xlmhg_O1_bound']