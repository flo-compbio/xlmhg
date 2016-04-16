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

"""Front-end for the XL-mHG test."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from math import isnan
import logging

import numpy as np

from . import mhg
from . import mhg_cython

logger = logging.getLogger(__name__)

def xlmhg_test(v, X=None, L=None, pval_thresh=None,
               K=None, table=None, skip_pval=False,
               use_alg1=False, tol=1e-12):
    """Perform the XL-mHG test using the Cython implementation.

    Parameters
    ----------
    v: np.ndarray of type np.uint8
        The ranked list. (Let N denote the length of the list.)
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
    skip_pval: bool, optional
        Whether to skip the calculation of the p-value. [False]
    use_alg1: bool, optional
        Whether to use PVAL1 (instead of PVAL2) for calculating the
        p-value. (Ignored if skip_pval=True.) [False]
    tol: float, optional
        The tolerance used for comparing floats. [1e-12]

    Returns
    -------
    stat: float
        The XL-mHG test statistic.
    n_star: int
        The (first) cutoff at which stat was attained.
        (0 if no cutoff was tested.)
    pval: float
        The XL-mHG p-value (either exact or an upper bound).
    """
    # type checks
    assert isinstance(v, np.ndarray)
    assert v.dtype == np.uint8
    if X is not None:
        assert isinstance(X, int)
    if L is not None:
        assert isinstance(L, int)
    if pval_thresh is not None:
        assert isinstance(pval_thresh, float)
    if K is not None:
        assert isinstance(K, int)
    if table is not None:
        assert isinstance(table, np.ndarray)
        assert table.dtype == np.longdouble
    assert isinstance(skip_pval, bool)
    assert isinstance(use_alg1, bool)
    assert isinstance(tol, float)

    N = v.size
    if X is None:
        X = 1
    if L is None:
        L = N

    # check values
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

    if K is None:
        # calculate K
        K = int(np.sum(v != 0))
    W = N - K
    
    if table is None:
        table = np.empty((K+1, W+1), dtype = np.longdouble)

    # calculate XL-mHG test statistic
    stat, n_star = mhg_cython.get_xlmhg_stat(v, N, K, X, L, tol)
    assert 0 < stat <= 1.0

    # calculate XL-mHG p-value (only if necessary)
    min_KL = min(K, L)
    upper_bound = min((min_KL-X+1)*stat, 1.0)
    if skip_pval:
        # do not calculate p-value at all
        pval = None
    elif stat == 1.0:
        # stat = 1.0 => pval = 1.0
        pval = 1.0
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

    if pval is not None and isnan(pval):
        # insufficient floating point precision, use bound
        logger.warning('Insufficient floating point precision for calculating '
                       'the exact p-value. Using upper bound instead.')
        pval = upper_bound

    return stat, n_star, pval
