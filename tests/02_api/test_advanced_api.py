# Copyright (c) 2016-2019 Florian Wagner
#
# This file is part of XL-mHG.

"""Tests for the advanced API (`get_xlmhg_test_result`). """

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import str as text

import numpy as np
import pytest

from xlmhg import mHGResult, xlmhg_test, get_xlmhg_test_result


def test_alg1(my_N, my_ind):
    """Test if we can use PVAL1 to calculate p-value."""
    res = get_xlmhg_test_result(my_N, my_ind, use_alg1=True)
    assert res.stat == 0.01393188854489164
    assert res.cutoff == 6
    assert res.pval == 0.0244453044375645


def test_O1bound(my_N, my_ind):
    """Test if we return the O(1)-bound if that's "<=" `pval_thresh`"""
    res = get_xlmhg_test_result(my_N, my_ind, pval_thresh=0.07,
                                exact_pval='if_necessary')
    assert res.pval == 0.0696594427244582


def test_ONbound(my_N, my_ind):
    """Test if we return the O(N)-bound instead of the exact
    p-value, if the bound is equal to or smaller than `pval_thresh`."""
    res = get_xlmhg_test_result(my_N, my_ind, pval_thresh=0.045,
                                exact_pval='if_necessary')
    assert res.pval == 0.04179566563467492


def test_significant1(my_N, my_ind):
    """Test if we return the exact p-value for a significant test when
    requested."""
    res = get_xlmhg_test_result(my_N, my_ind, pval_thresh=0.07,
                                exact_pval='if_significant')
    assert res.pval == 0.0244453044375645


def test_significant2(my_N, my_ind):
    """Test if we return the exact p-value for a significant test when
    requested, even if we don't need to calculate it in order to determine that
    the test is significant."""
    res = get_xlmhg_test_result(my_N, my_ind, pval_thresh=0.045,
                                exact_pval='if_significant')
    assert res.pval == 0.0244453044375645


def test_pval_necessary(my_N, my_ind):
    """Test if we return the p-value when it is necessary."""
    res = get_xlmhg_test_result(my_N, my_ind, pval_thresh=0.04,
                                exact_pval='if_necessary')
    assert res.pval == 0.0244453044375645


def test_lowerbound(my_N, my_ind):
    """Test if we return the O(1)-bound when stat > pval_thresh."""
    res = get_xlmhg_test_result(my_N, my_ind, pval_thresh=0.01,
                                exact_pval='if_necessary')
    assert res.pval == 0.0696594427244582


def test_limit_pval(my_incredible_pval_v):
    """Test differential accuracy of PVAL1 and PVAL2."""
    # PVAL1 algorithm should handle this without problems
    N = my_incredible_pval_v.size
    ind = np.uint16(np.nonzero(my_incredible_pval_v)[0])
    res = get_xlmhg_test_result(N, ind)
    assert res.stat == 1.5112233509292993e-216
    assert res.cutoff == 200
    assert res.pval == res.stat

    res = get_xlmhg_test_result(N, ind, use_alg1=True)
    # PVAL2 algorithm should report an invalid p-value
    # (either <= 0 or unrealistically large; in this case < 0)
    # and the front-end should replace that with the O(1)-bound
    assert res.stat == 1.5112233509292993e-216
    assert res.cutoff == 200
    assert res.stat < res.pval < 1e-200


def test_non_contiguous(my_N, my_ind):
    """Test if non-contiguous arrays result in a ValueError."""
    with pytest.raises(ValueError):
        result = get_xlmhg_test_result(my_N, my_ind[::-1])


def test_table_too_small(my_N, my_ind):
    """Test if ValueError is raised when the supplied array is too small."""
    K = my_ind.size
    with pytest.raises(ValueError):
        table = np.empty(((my_N-K), (my_N-K)), np.longdouble)
        result = get_xlmhg_test_result(my_N, my_ind, table=table)


def test_params(my_N, my_ind, my_v):
    result = get_xlmhg_test_result(my_N, my_ind, X=1)
    assert isinstance(result, mHGResult)
    result = get_xlmhg_test_result(my_N, my_ind, L=my_N)
    assert isinstance(result, mHGResult)
    result = get_xlmhg_test_result(my_N, my_ind, pval_thresh=0.05)
    assert isinstance(result, mHGResult)
    table = np.empty((my_N + 1, my_N + 1), np.longdouble)
    result = get_xlmhg_test_result(my_N, my_ind, table=table)
    assert isinstance(result, mHGResult)


