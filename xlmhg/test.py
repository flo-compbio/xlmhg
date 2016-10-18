# Copyright (c) 2016 Florian Wagner
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

"""Python API for performing XL-mHG tests."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import sys
from math import isnan
import logging

import numpy as np

from . import mhg
try:
    # This is a duct-tape fix for the Google App Engine, on which importing
    # the C extension fails.
    from . import mhg_cython
except ImportError:
    print('Warning (xlmhg): Failed to import the "mhg_cython" C extension.'
          'Falling back to the pure Python implementation, which is very '
          'slow.', file=sys.stderr)
    from . import mhg as mhg_cython

from .result import mHGResult

logger = logging.getLogger(__name__)


def get_xlmhg_O1_bound(stat, K, X, L):
    """Calculate the O(1)-bound for the XL-mHG p-value."""
    assert isinstance(stat, (float, np.float))
    assert isinstance(K, (int, np.integer))
    assert isinstance(X, (int, np.integer))
    assert isinstance(L, (int, np.integer))

    min_KL = min(K, L)
    upper_bound = min((min_KL-X+1)*stat, 1.0)
    return upper_bound

def get_xlmhg_test_result(N, indices, X=None, L=None,
                          exact_pval='always', # if_necessary, if_significant
                          pval_thresh=None, escore_pval_thresh=None,
                          table=None, use_alg1=False, tol=1e-12):
    """Perform an XL-mHG test.

    This function accepts a list in the form of a numpy ``indices`` array
    containing the indices of the non-zero elements (sorted), along with the
    length ``N`` of the list. It returns an `mHGResult` object.

    Parameters
    ----------
    N, int
        The length of the list.
    indices: 1-dim `numpy.ndarray` with ``dtype`` = numpy.uint16
        Sorted list of indices corresponding to the "1"s in the ranked list.
    X: int, optional
        The ``X`` parameter. Should be between 1 and K (inclusive), where K
        is the length of ``indices``. [1]
    L: int, optional
        The ``L`` parameter. Should be between 1 and ``N`` (inclusive). If
        `None`, this parameter will be set to ``N`` [None]
    exact_pval: str, enumerated
        Valid values are: 'always', 'if_significant', and 'if_necessary'.
        Determines in which cases exact p-values should be calculated. This
        option helps users avoid the time-consuming calculation of an exact
        p-value in cases where they do not require it, which can lead to
        significant performance gains. ['always']

        Specifically, this setting (in conjunction with ``pval_thresh``)
        determines in which cases the PVAL-THRESH algorithm is invoked to
        efficiently determine whether the test is significant. This algorithm
        first tries to make this determination by calculating O(1)- and O(N)-
        bounds of the XL-mHG p-value. Only if this fails to give a conclusive
        answer, an O(N^2)-algorithm is used to calculate the exact p-value.

        Note that whenever 'if_necessary' or 'if_significant' is
        specified, a significance level (p-value threshold; argument
        ``pval_thresh``) must be specified as well.
    pval_thresh: float, optional
        The significance threshold, i.e., the p-value below which the test
        should be considered statistically significant. Note that this
        argument must be given whenever the ``escore_pval_thresh`` argument is
        given. [None]
    escore_pval_thresh: float, optional
        The significance threshold to be used in the calculation of an E-score.
        The E-score is a measure of the strength of enrichment that is similar
        to "fold enrichment". [None]
    table: `numpy.ndarray` with ``ndim=2`` and ``dtype=numpy.longdouble``, optional
        The dynamic programming table. Size has to be at least (K+1) x (W+1).
        Providing this array avoids memory reallocation when conducting
        multiple tests. [None]
    use_alg1: bool, optional
        Whether to use PVAL1 (instead of PVAL2) for calculating the
        p-value. [False]
    tol: float, optional
        The tolerance used for comparing floats. [1e-12]

    Returns
    -------
    `mHGResult`
        The test result.
    """
    # type checks
    assert isinstance(N, (int, np.integer))
    assert isinstance(indices, np.ndarray) and indices.ndim == 1 and\
        np.issubdtype(indices.dtype, np.uint16)
    if X is not None:
        assert isinstance(X, (int, np.integer))
    if L is not None:
        assert isinstance(L, (int, np.integer))
    assert isinstance(exact_pval, str)
    if pval_thresh is not None:
        assert isinstance(pval_thresh, (float, np.float))
    if escore_pval_thresh is not None:
        assert isinstance(escore_pval_thresh, (float, np.float))
    if table is not None:
        assert isinstance(table, np.ndarray) and table.ndim == 2 and \
            np.issubdtype(table.dtype, np.longdouble)
    assert isinstance(use_alg1, (bool, np.bool_))
    assert isinstance(tol, (float, np.float))

    # assign default values, if None
    K = indices.size
    if X is None:
        X = 1
    if L is None:
        L = N

    ### check whether parameter values are in range
    if not indices.flags.c_contiguous:
        raise ValueError('Array is not C-contiguous! Try '
                         '"np.ascontiguousarray()".')
    if N > 65536:
        raise ValueError(
            'Length of list cannot exceed 65536.'
        )
    if not (1 <= X <= N):
        raise ValueError(
            'Invalid value X=%d; should be >= 1 and <= %d.' %(X, N)
        )
    if not (1 <= L <= N):
        raise ValueError(
            'Invalid value L=%d; should be >= 1 and <= %d.' %(L, N)
        )
    if pval_thresh is not None and not (0.0 <= pval_thresh <= 1.0):
        raise ValueError(
            'Invalid value pval_thresh=%.1e; should be in [0,1).' % pval_thresh
        )
    if escore_pval_thresh is not None and \
            not (0.0 <= escore_pval_thresh <= 1.0):
        raise ValueError(
            'Invalid value escore_pval_thersh=%.1e; should be in [0,1).'
                % escore_pval_thresh
        )
    if not (0.0 <= tol < 1.0):
        raise ValueError('Invalid value tol=%.1e; should be in [0,1).' % tol)

    ### check if combination of argument values is valid
    if exact_pval not in ['always', 'if_significant', 'if_necessary']:
        raise ValueError('Invalid value exact_pval="%s".'
                         'Must be "always", "if_necessary", '
                         'or "if_significant".')

    if exact_pval in ['if_necessary', 'if_significant'] and \
                    pval_thresh is None:
        raise ValueError('Missing argument: exact_pval=%s requires '
                         'a significance level to be specified (pval_thresh).')

    if escore_pval_thresh is not None and pval_thresh is None:
        raise ValueError('Missing argument: Setting escore_pval_thresh '
                         'requires a significance level to be specified'
                         '(pval_thresh).')

    ### check if s=1.0 by definition
    min_KL = min(K, L)
    if X > min_KL:
        # `X` is larger than the largest possible number of 1's above any of
        # the cutoffs considered. By definition, s=1.0, and therefore p=1.0.
        stat = 1.0
        cutoff = 0
        pval = 1.0
        result = mHGResult(N, indices, X, L, stat, cutoff, pval,
                           pval_thresh=pval_thresh,
                           escore_pval_thresh=escore_pval_thresh)
        return result

    # If an array for the dynamic programming table is supplied, make sure it's
    # large enough. Otherwise, create an empty array.
    W = N - K
    if table is None:
        table = np.empty((K+1, W+1), dtype = np.longdouble)
    elif table.shape[0] < K+1 or table.shape[1] < W+1:
        raise ValueError('Supplied array for dynamic programming table not'
                         'large enough. It is: %d x %d, but must be at least '
                         '%d x %d ((K+1) x (W+1)).'
                         % (table.shape[0], table.shape[1], K+1, W+1))

    ### Step 1: Calculate XL-mHG test statistic.
    stat, cutoff = mhg_cython.get_xlmhg_stat(indices, N, K, X, L, tol)
    assert 0.0 <= stat <= 1.0

    # check for special cases
    pval = None
    if stat == 1.0:
        # stat = 1.0 => pval = 1.0
        pval = 1.0
    elif stat == 0.0:
        logger.warning('Insufficient floating point precision for calculating '
                       'or reporting the exact XL-mHG test statistic; the '
                       'true value is too small. Using "0" instead.'
                       '(The XL-mHG p-value will also be reported as "0".)')
        pval = 0.0

    if pval is not None:
        # stop here
        result = mHGResult(N, indices, X, L, stat, cutoff, pval,
                           pval_thresh=pval_thresh,
                           escore_pval_thresh=escore_pval_thresh)
        return result

    ### Step 2: Determine whether we need to calculate the exact p-value
    # If a significance level (p-value threshold) is specified, and the
    # `exact_pval` argument is not set to "always", then our first job is to
    # determine whether the XL-mHG p-value is significant our not. Otherwise,
    # we can skip this step.
    pval_is_significant = None
    # calculate the O(1)-bound of the XL-mHG p-value
    # O1_upper_bound = min((min_KL - X + 1) * stat, 1.0)
    O1_upper_bound = get_xlmhg_O1_bound(stat, K, X, L)
    if pval_thresh is not None and exact_pval != 'always':

        # use PVAL-THRESH algorithm to determine if p-value is significant
        if stat > pval_thresh and not mhg.is_equal(stat, pval_thresh, tol):
            # The test statistic is larger than the significance threshold.
            # Since the test statistic serves a lower bound for the p-value,
            # this means that the test cannot be significant.
            # => Report upper bound instead of true p-value.
            pval_is_significant = False
            pval = O1_upper_bound

        elif O1_upper_bound <= pval_thresh or \
                mhg.is_equal(O1_upper_bound, pval_thresh, tol):
            # The upper bound is "<=" the significance threshold.
            # This means that the test *is* significant.
            # => Depending on the value of `exact_pval`, we report either
            #    the upper bound or the exact p-value (see Step 3).
            pval = O1_upper_bound
            pval_is_significant = True

        else:
            # O(1)-bound was inconclusive
            # => calculate O(N)-bound
            ON_upper_bound = mhg_cython.get_xlmhg_ON_bound(N, K, X, L, stat,
                                                           tol)
            if ON_upper_bound <= pval_thresh or \
                mhg.is_equal(ON_upper_bound, pval_thresh, tol):
                # The upper bound is "<=" the significance threshold.
                # This means that the test *is* significant.
                # => Depending on the value of `exact_pval`, we report either
                #    the upper bound or the exact p-value (see Step 3).
                pval = ON_upper_bound
                pval_is_significant = True

            else:
                # The bound is still larger than the significance threshold.
                # => We need to calculate the exact p-value in order to
                #    determine whether the test is significant or not.
                pass

    ### Step 3: Calculate the exact p-value (if required).
    # There are three conditions (not mutually exclusive) which require that
    # we calculate the exact p-value:
    # 1. The `exact_pval` argument is set to "always".
    # 2. The `exact_pval` argument is set to "if_significant", and the test
    #    was found to be significant in Step 2 (based on upper bounds).
    # 3. A significance level was specified, and we were unable to decide
    #    whether the test is significant without calculating the exact p-value.
    if exact_pval == 'always' or \
            pval_is_significant is None or \
            (exact_pval == 'if_significant' and pval_is_significant):
        # we need to calculate the exact p-value
        if not use_alg1:
            # use PVAL2 algorithm
            pval = mhg_cython.get_xlmhg_pval2(N, K, X, L, stat, table, tol)
        else:
            # use PVAL1 algorithm
            pval = mhg_cython.get_xlmhg_pval1(N, K, X, L, stat, table, tol)


    if isnan(pval) or pval <= 0 or \
            (pval > O1_upper_bound and
                 (not mhg.is_equal(pval, O1_upper_bound, tol))):
        # insufficient floating point precision for calculating p-value,
        # report O(1)-bound instead
        logger.warning('Insufficient floating point precision for calculating '
                       'the exact XL-mHG p-value. Using upper bound instead.')
        pval = O1_upper_bound

    # generate result object
    result = mHGResult(N, indices, X, L, stat, cutoff, pval,
                       pval_thresh=pval_thresh,
                       escore_pval_thresh=escore_pval_thresh)
    return result


def xlmhg_test(v, X=None, L=None, table=None):
    """Perform an XL-mHG test (simplified interface).

    This function accepts a vector containing zeros and ones, and returns
    a 3-tuple with the XL-mHG test statistic, cutoff, and p-value.

    Parameters
    ----------
    v: 1-dim `numpy.ndarray` of integers
        The ranked list. All non-zero elements are considered "1"s.
        (Let N denote the length of the list.)
    X: int, optional
        The ``X`` parameter. [1]
    L: int, optional
        The ``L`` parameter. [N]
    table: np.ndarray with ``ndim=2`` and ``dtype=numpy.longdouble``, optional
        The dynamic programming table. Size has to be at least (K+1) x (W+1),
        with W = N-K. Providing this array avoids memory reallocation when
        conducting multiple tests. [None]

    Returns
    -------
    stat: float
        The XL-mHG test statistic.
    cutoff: int
        The (first) cutoff at which stat was attained.
        (0 if no cutoff was tested.)
    pval: float
        The XL-mHG p-value (either exact or an upper bound).
    """
    assert isinstance(v, np.ndarray) and v.ndim == 1 \
        and np.issubdtype(v.dtype, np.integer)
    if v.size > 65536:
        raise ValueError('List is too long. The maximum length supported is '
                         ' 65536.')
    indices = np.uint16(np.nonzero(v)[0])
    N = v.size
    result = get_xlmhg_test_result(N, indices, X, L, table=table)
    return result.stat, result.cutoff, result.pval



