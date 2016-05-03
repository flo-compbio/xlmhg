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

"""Tests for the XL-mHG Python front-end (`test.py`). """

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import str as text

import numpy as np
import pytest

from xlmhg import mHGResult, xlmhg_test, get_xlmhg_test_result


@pytest.fixture
def my_v():
    v = np.uint8([1, 0, 1, 1, 0, 1] + [0] * 12 + [1, 0])  # example from paper
    return v


@pytest.fixture
def my_much_too_long_v():
    v = np.uint8([1, 0, 1, 1, 0, 1] + [0] * 100000)
    return v


@pytest.fixture
def my_indices(my_v):
    indices = np.uint16(np.nonzero(my_v)[0])
    return indices


@pytest.fixture
def my_incredible_stat_v():
    # test statistic is smaller than smallest double larger than zero
    v = np.uint8([1]*500 + [0]* 1500)
    return v


@pytest.fixture
def my_incredible_pval_v():
    # PVAL1 fails, PVAL2 works
    v = np.uint8([1]*200 + [0]* 800)
    return v


def test_mhg(my_v):
    # test regular mHG test
    res = xlmhg_test(my_v)
    assert res[0] == 0.01393188854489164
    assert res[1] == 6
    assert res[2] == 0.0244453044375645


def test_alg1(my_v):
    # test if we can use PVAL1 to calculate p-value
    res = xlmhg_test(my_v, use_alg1=True)
    assert res[0] == 0.01393188854489164
    assert res[1] == 6
    assert res[2] == 0.0244453044375645


def test_O1bound(my_v):
    # test if we return the O(1)-bound if that's equal to or smaller than
    # pval_thresh
    res = xlmhg_test(my_v, pval_thresh=0.07)
    assert res[2] == 0.0696594427244582


def test_ONbound(my_v):
    # test if we return the O(N)-bound instead of calculating the p-value if
    # the bound is equal to or smaller than pval_thresh
    res = xlmhg_test(my_v, pval_thresh=0.045)
    assert res[2] == 0.04179566563467492


def test_lowerbound(my_v):
    # test if we return the O(1)-bound when stat > pval_thresh
    res = xlmhg_test(my_v, pval_thresh=0.01)
    assert res[2] == 0.0696594427244582


def test_X(my_v):
    # test effect of X
    res = xlmhg_test(my_v, X=4)
    assert res[2] == 0.01876934984520124


def test_L(my_v):
    res = xlmhg_test(my_v, L=6)
    assert res[2] == 0.019801341589267284


def test_result(my_indices, my_v):
    N = my_v.size
    result = get_xlmhg_test_result(N, my_indices)
    assert isinstance(result, mHGResult)


def test_limit_stat(my_incredible_stat_v):
    res = xlmhg_test(my_incredible_stat_v)
    # print('Test')
    # print(res)
    assert res[0] == 0.0
    assert res[1] == 500
    assert res[2] == 0.0


def test_limit_pval(my_incredible_pval_v):
    # PVAL1 algorithm should handle this without problems
    res = xlmhg_test(my_incredible_pval_v)
    assert res[0] == 1.5112233509292993e-216
    assert res[1] == 200
    assert res[2] == res[0]

    res = xlmhg_test(my_incredible_pval_v, use_alg1=True)
    # PVAL2 algorithm should report an invalid p-value
    # (either <= 0 or unrealistically large; in this case < 0)
    # and the front-end should replace that with the O(1)-bound
    assert res[0] == 1.5112233509292993e-216
    assert res[1] == 200
    assert res[2] < 1e-200


def test_non_contiguous(my_indices, my_v):
    N = my_v.size
    with pytest.raises(ValueError):
        result = get_xlmhg_test_result(N, my_indices[::-1])


def test_list_too_long(my_much_too_long_v):
    with pytest.raises(ValueError):
        result = xlmhg_test(my_much_too_long_v)


def test_table_too_small(my_indices, my_v):
    N = my_v.size
    K = my_indices.size
    with pytest.raises(ValueError):
        table = np.empty(((N-K), (N-K)), np.longdouble)
        result = get_xlmhg_test_result(N, my_indices, table=table)


def test_params(my_indices, my_v):
    N = my_v.size
    result = get_xlmhg_test_result(N, my_indices, X=1)
    assert isinstance(result, mHGResult)
    result = get_xlmhg_test_result(N, my_indices, L=N)
    assert isinstance(result, mHGResult)
    result = get_xlmhg_test_result(N, my_indices, pval_thresh=0.05)
    assert isinstance(result, mHGResult)
    table = np.empty((N+1, N+1), np.longdouble)
    result = get_xlmhg_test_result(N, my_indices, table=table)
    assert isinstance(result, mHGResult)