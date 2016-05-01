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

"""Tests for the Cython implementation of the XL-mHG E-score."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import str as text

import itertools as it
import math

import pytest
import numpy as np
from scipy.stats import hypergeom

from xlmhg import mhg, mhg_cython, xlmhg_test


def calculate_escore(v, K, X, L, hgp_thresh, tol):
    N = v.size
    k = 0
    escore = 0.0
    for i in np.nonzero(v[:L])[0]:
        k += 1
        if k >= X:
            e = k / (((i + 1) * K) / float(N))
            if e > escore and not mhg.is_equal(e, escore, tol):
                hgp = hypergeom.sf(k - 1, N, K, i + 1)
                if hgp <= hgp_thresh or mhg.is_equal(hgp, hgp_thresh, tol):
                    escore = e
    if escore == 0:
        escore = float('nan')
    return escore


def test_mhg_escore():
    # test if mHG E-score implementation is correct
    # tests random lists with N = 20 and K = 5
    tol = 1e-11
    seed = 123456789
    num_lists = 500
    default_tol = mhg_cython.get_default_tol()

    N = 20
    K = 5
    X = 1
    L = N
    C = np.int64(list(it.combinations(range(N),K)))
    p = C.shape[0]
    np.random.seed(seed)
    for i in range(num_lists):
        idx = np.random.randint(p)
        v = np.zeros(N, dtype = np.uint8)
        v[C[idx,:]] = 1
        stat, cutoff, pval = xlmhg_test(v, X, L, K=K)
        escore_ref = calculate_escore(v, K, X, L, pval, tol)
        escore = mhg_cython.get_xlmhg_escore(v, N, K, X, L, pval)
        assert escore > 0 and mhg.is_equal(escore, escore_ref, tol=tol)


def test_xlmhg_escore():
    # test if XL-mHG E-score implementation is correct
    # uses a particular example vector,
    # and goes over all combinations of X and L
    v = np.uint8([1,0,1,1,0,1] + [0]*12 + [1,0]) # example from paper
    N = v.size
    K = int(np.sum(v != 0))
    tol = 1e-11

    total = 0
    larger = 0
    assert N == 20 and K == 5
    for L in range(1, N+1):
        for X in range(1, N+1):
            total += 1
            stat, cutoff, pval = xlmhg_test(v, X, L, K=K)
            # stat, n_star, _ = xlmhg_test(v, X, L)
            escore_ref = calculate_escore(v, K, X, L, pval, tol)
            escore = mhg_cython.get_xlmhg_escore(v, N, K, X, L, pval)
            if escore > 0:
                larger += 1
            assert math.isnan(escore) or escore > 0
            assert (math.isnan(escore) and math.isnan(escore_ref)) or \
                   mhg.is_equal(escore, escore_ref, tol=tol), \
                   '%s / %s / %s' %(repr(v), repr(X), repr(L))
    print('E-score was valid in %d / %d cases.' % (larger, total))