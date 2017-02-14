# from __future__ import (absolute_import, division,
#                         print_function, unicode_literals)
# from builtins import *

import pkg_resources
# import os

__version__ = pkg_resources.require('xlmhg')[0].version

from .result import mHGResult
from .test import get_xlmhg_O1_bound, xlmhg_test, get_xlmhg_test_result
from .visualize import get_result_figure

#__all__ = ['get_xlmhg_linear_bound', 'xlmhg_test', 'test',
#           'mHGResult', 'get_xlmhg_test_result',
#xlmhg_test           'get_result_figure']