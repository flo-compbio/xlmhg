import pkg_resources

__version__ = pkg_resources.require('xlmhg')[0].version

from .result import mHGResult
from .test import get_xlmhg_O1_bound, xlmhg_test, get_xlmhg_test_result
from .visualize import get_result_figure
