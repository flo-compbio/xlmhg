# from __future__ import (absolute_import, division,
#                         print_function, unicode_literals)
# from builtins import *

import pkg_resources
# import os

__version__ = pkg_resources.require('xlmhg')[0].version

from .result import mHGResult
from .test import xlmhg_test, get_xlmhg_test_result
from .visualize import get_result_figure

__all__ = ['xlmhg_test',
           'mHGResult', 'get_xlmhg_test_result',
           'get_result_figure']