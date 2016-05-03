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

"""Python front-end for the XL-mHG test."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from math import isnan
import logging

import numpy as np

from . import mhg, mhg_cython
from .result import mHGResult

logger = logging.getLogger(__name__)


def get_xlmhg_test_result(N, indices, X=None, L=None, pval_thresh=None,
                          table=None, use_alg1=False, tol=1e-12):
    """Perform the XL-mHG test using the Cython implementation.

    This function accepts a list in the form of a numpy `indices` array
    containing the indices of the non-zero elements (sorted), along with the
    length `N` of the list. It returns an `mHGResult` object.

    Parameters
    ----------
    N, int
        The length of the list.
    indices: 1-dim np.ndarray with dtype = np.uint16
        Sorted list of indices corresponding to the "1"s in the ranked list.
    X: int, optional
        The ``X`` parameter. [1]
    L: int, optional
        The ``L`` parameter. [N]
    pval_thresh: float, optional
        Use the PVAL-THRESH algorithm to determine whether the XL-mHG p-value
        is equal to or smaller than the specified value. The algorithm tries to
        use lower and upper bounds instead of calculating the exact p-value,
        which can be significantly faster. (Ignored if skip_pval=True.) [None]
    table: np.ndarray with ndim=2 and dtype=np.float64, optional
        The dynamic programming table. Size has to be at least (K+1) x (W+1).
        Providing this array avoids memory reallocation when conducting
        multiple tests. [None]
    use_alg1: bool, optional
        Whether to use PVAL1 (instead of PVAL2) for calculating the
        p-value. (Ignored if skip_pval=True.) [False]
    tol: float, optional
        The tolerance used for comparing floats. [1e-12]

    Returns
    -------
    `mHGResult`
        The test result.
    """
    # type checks
    assert isinstance(N, int)
    assert isinstance(indices, np.ndarray) and indices.ndim == 1 and\
        np.issubdtype(indices.dtype, np.uint16)
    if X is not None:
        assert isinstance(X, (int, np.integer))
    if L is not None:
        assert isinstance(L, (int, np.integer))
    if pval_thresh is not None:
        assert isinstance(pval_thresh, float)
    if table is not None:
        assert isinstance(table, np.ndarray) and table.ndim == 2 and \
            np.issubdtype(table.dtype, np.longdouble)
    assert isinstance(use_alg1, bool)
    assert isinstance(tol, float)

    # assign default values, if None
    K = indices.size
    if X is None:
        X = 1
    if L is None:
        L = N

    # check whether parameter values are in range
    if not indices.flags.c_contiguous:
        raise ValueError('Array is not C-contiguous! Try '
                         '"np.ascontiguousarray()".')
    if N > 35536:
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
    if not (0.0 <= tol < 1.0):
        raise ValueError('Invalid value tol=%.1e; should be in [0,1)' %(tol))

    W = N - K
    if table is None:
        table = np.empty((K+1, W+1), dtype = np.longdouble)
    elif table.shape[0] < K+1 or table.shape[1] < W+1:
        raise ValueError('Supplied array for dynamic programming table not'
                         'large enough. It is: %d x %d, but must be at least '
                         '%d x %d ((K+1) x (W+1)).'
                         % (table.shape[0], table.shape[1], K+1, W+1))

    # calculate XL-mHG test statistic
    stat, cutoff = mhg_cython.get_xlmhg_stat(indices, N, K, X, L, tol)
    assert 0.0 <= stat <= 1.0

    # calculate XL-mHG p-value (only if necessary)
    min_KL = min(K, L)
    upper_bound = 1.0
    if X <= min_KL:
        upper_bound = min((min_KL-X+1)*stat, 1.0)
    if stat == 1.0:
        # stat = 1.0 => pval = 1.0
        pval = 1.0
    elif stat == 0.0:
        logger.warning('Insufficient floating point precision for calculating '
                       'or reporting the exact XL-mHG test statistic; the '
                       'true value is too small. Reporting 0 instead.'
                       '(The XL-mHG p-value will also be reported as 0.)')
        pval = 0.0
    elif pval_thresh is not None:
        # PVAL-THRESH algorithm
        if stat > pval_thresh and not mhg.is_equal(stat, pval_thresh, tol):
            # test statistic is larger than the significance threshold
            # => report upper bound instead of true p-value
            pval = upper_bound
        elif upper_bound <= pval_thresh or \
                mhg.is_equal(upper_bound, pval_thresh, tol):
            # upper bound is "<=" the significance threshold
            # report upper bound
            pval = upper_bound
        else:
            # calculate O(N)-bound
            ON_upper_bound = mhg_cython.get_xlmhg_bound(N, K, X, L, stat, tol)
            if ON_upper_bound <= pval_thresh or \
                mhg.is_equal(ON_upper_bound, pval_thresh, tol):
                pval = ON_upper_bound
            else:
                # O(N) bound is still larger than the significance threshold
                # => calculate exact p-value
                if not use_alg1:
                    pval = mhg_cython.get_xlmhg_pval2(N, K, X, L, stat,
                                                      table, tol)
                else:
                    pval = mhg_cython.get_xlmhg_pval1(N, K, X, L, stat,
                                                      table, tol)
    else:
        # calculate p-value
        if not use_alg1:
            pval = mhg_cython.get_xlmhg_pval2(N, K, X, L, stat, table, tol)
        else:
            pval = mhg_cython.get_xlmhg_pval1(N, K, X, L, stat, table, tol)

    if stat != 0.0 and (isnan(pval) or pval <= 0 or \
            (pval > upper_bound and not mhg.is_equal(pval, upper_bound, tol))):
        # insufficient floating point precision for calclating p-value,
        # report O(1)-bound instead
        logger.warning('Insufficient floating point precision for calculating '
                       'the exact XL-mHG p-value. Reporting upper bound '
                       'instead. (stat=%.2e, pval=%.2e))' % (stat, pval))
        pval = upper_bound

    # generate result object
    result = mHGResult(N, indices, X, L, stat, cutoff, pval,
                       pval_thresh=pval_thresh)
    return result


def xlmhg_test(v, X=None, L=None, pval_thresh=None,
               table=None, use_alg1=False, tol=1e-12):
    """Perform the XL-mHG test using the Cython implementation.

    This function accepts a vector containing zeros and ones, and returns
    a 3-tuple with the XL-mHG test statistic, cutoff, and p-value.

    Parameters
    ----------
    v: 1-dim np.ndarray of integers
        The ranked list. All non-zero elements are considered "1"s.
        (Let N denote the length of the list.)
    X: int, optional
        The ``X`` parameter. [1]
    L: int, optional
        The ``L`` parameter. [N]
    pval_thresh: float, optional
        Use the PVAL-THRESH algorithm to determine whether the XL-mHG p-value
        is equal to or smaller than the specified value. The algorithm tries to
        use lower and upper bounds instead of calculating the exact p-value,
        which can be significantly faster. (Ignored if skip_pval=True.) [None]
    table: np.ndarray with ndim=2 and dtype=np.float64, optional
        The dynamic programming table. Size has to be at least (K+1) x (W+1).
        Providing this array avoids memory reallocation when conducting
        multiple tests. [None]
    use_alg1: bool, optional
        Whether to use PVAL1 (instead of PVAL2) for calculating the
        p-value. (Ignored if skip_pval=True.) [False]
    tol: float, optional
        The tolerance used for comparing floats. [1e-12]

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
    result = get_xlmhg_test_result(N, indices, X, L,
                                   pval_thresh=pval_thresh, table=table,
                                   use_alg1=use_alg1, tol=tol)
    return result.stat, result.cutoff, result.pval



