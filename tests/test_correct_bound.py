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

"""Tests for Cython implementation of the XL-mHG bounds."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import str as text

import numpy as np
from scipy.stats import hypergeom

from xlmhg import mhg
from xlmhg import mhg_cython

def calculate_bound(N, K, X, L, stat, S):
    """Calculate the O(N) upper bound when we know s_(k,w), for all (k,w)."""
    assert isinstance(stat, float)
    assert isinstance(S, np.ndarray)

    min_KL = min(K, L)
    
    W = N-K
    assert S.shape == (K+1, W+1)
    
    if stat == 1.0:
        return 1.0, 1, K
    
    if S[min_KL, 0] > stat:
        # R is empty
        return 0.0
    
    # calculate k_min
    k_min = int(np.sum(S[:min_KL, 0] > stat))
    
    # calculate k_max
    if L > K and S[K, L-K] > stat:
        # S[K, L] is not in R, so k_max = K
        k_max = K
    else:
        k = min_KL
        w = np.nonzero(S[min_KL,:] <= stat)[0][-1]
        n = k+w
        while S[k, w] <= stat:
            k -= 1
            w += 1
        k_max = k+1 # we need the last k which is in R
        
    return min((k_max-k_min+1)*stat, 1.0), k_min, k_max

def test_bound():
    #N = 20
    #K = 5
    N = 50
    K = 10
    tol = 1e-12
    
    W = N-K
    table = np.empty((K+1, W+1), dtype=np.longdouble)

    # calculate hypergeometric p-values for all configurations
    configs = np.ones((K+1, W+1), dtype=np.float64)
    for k in range(1, K+1):
        for w in range(W):
            n = k+w
            configs[k, w] = hypergeom.sf(k-1, N, K, n)
            
    # test all possible combinations of X and L
    tests = 0
    smaller = 0
    for X in range(1, N+1):
        for L in range(N, 0, -1):
            #if X > L: continue
            
            min_KL = min(K, L)

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
                # calculate and validate bound
                bound_ref, k_min, k_max = calculate_bound(N, K, X, L, stat, S)
                bound = mhg_cython.get_xlmhg_bound(N, K, X, L, stat)
                assert bound == bound_ref, \
                        'X=%d, L=%d, stat=%.3e => k_min=%d, k_max=%d' \
                        %(X, L, stat, k_min, k_max)

                # make sure bound is >= actual p-value
                pval = mhg_cython.get_xlmhg_pval2(N, K, L, X, stat, table)
                assert bound >= pval or mhg.is_equal(bound, pval, tol)

                # make sure O(1) bound is >= this bound
                assert bound <= min(K*stat, 1.0) or \
                        mhg.is_equal(bound, min(K*stat, 1.0), tol)

                tests += 1
                if bound < min(K*stat, 1.0) and not \
                        mhg.is_equal(bound, min(K*stat, 1.0), tol):
                    smaller += 1

    print('Calculated %d p-values, based on %d configurations!'
          %(tests, configs.size))
    print('In %d / %d cases, the O(N)-bound was smaller than the O(1)-bound.'
          %(smaller, tests))
