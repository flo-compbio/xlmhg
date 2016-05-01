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

"""Tests for the Cython implementations of the XL-mHG p-value.."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import str as text

import numpy as np
from scipy.stats import hypergeom

from xlmhg import mhg, mhg_cython

def test_cross():
    """Compares p-values calculated using PVAL1 and PVAL2."""
    N = 50
    K = 10

    #tol = 1e-11
    tol = 1e-8

    W = N-K
    table = np.empty((K+1, W+1), dtype=np.longdouble)

    # calculate hypergeometric p-values for all configurations
    configs = np.ones((K+1, W+1), dtype=np.float64)
    for k in range(1, K+1):
        for w in range(W):
            n = k+w
            configs[k, w] = hypergeom.sf(k-1, N, K, n)

    tests = 0
    for X in range(1, N+1):
        for L in range(N, 0, -1):
            # calculate all possible XL-mHG test statistics
            S = np.ones((K+1, W+1), dtype=np.float64)
            for n in range(L+1):
                k = min(K, n)
                w = n-k
                while k >= X and w <= W and n <= L:
                    S[k, w] = configs[k, w]
                    k -= 1
                    w += 1

            all_stat = np.sort(np.unique(S.ravel()))[::-1]

            for stat in all_stat:
                pval1 = mhg_cython.get_xlmhg_pval1(N, K, X, L, stat, table)
                pval2 = mhg_cython.get_xlmhg_pval2(N, K, X, L, stat, table)
                tests += 1
                assert mhg.is_equal(pval1, pval2, tol=tol)

    print('Calculated %d bounds, based on %d configurations.'
          %(tests, configs.size))
