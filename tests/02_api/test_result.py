# Copyright (c) 2016-2019 Florian Wagner
#
# This file is part of XL-mHG.

"""Tests for the `mHGResult` class (in `result.py`)."""

from copy import deepcopy

import pytest
import numpy as np

from xlmhg import get_xlmhg_test_result, mHGResult


@pytest.fixture
def my_result(my_v, my_ind):
    N = my_v.size
    K = my_ind.size
    X = 1
    L = N
    #stat, cutoff, pval = xlmhg_test(my_indices, X, L)
    #result = mHGResult(my_indices, N, X, L, stat, cutoff, pval)
    result = get_xlmhg_test_result(N, my_ind, X, L)
    return result


def test_basic(my_result, my_v, my_ind):
    assert isinstance(my_result, mHGResult)
    assert isinstance(repr(my_result), str)
    assert isinstance(str(my_result), str)
    assert isinstance(my_result.hash, str)
    assert np.array_equal(my_result.indices, my_ind)
    assert np.array_equal(my_result.v, my_v)
    assert isinstance(my_result.k, int)

    other = deepcopy(my_result)
    assert other is not my_result
    assert other == my_result
    other.pval = 0.86213
    assert other != my_result

    assert isinstance(my_result.N, int)
    assert my_result.N == my_v.size
    assert isinstance(my_result.escore, float)