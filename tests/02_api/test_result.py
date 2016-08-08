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

"""Tests for the `mHGResult` class (in `result.py`)."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import str as text
from builtins import int as newint

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
    assert isinstance(text(my_result), text)
    assert isinstance(my_result.hash, text)
    assert np.array_equal(my_result.indices, my_ind)
    assert np.array_equal(my_result.v, my_v)
    assert isinstance(my_result.k, newint)

    other = deepcopy(my_result)
    assert other is not my_result
    assert other == my_result
    other.pval = 0.86213
    assert other != my_result

    assert isinstance(my_result.N, newint)
    assert my_result.N == my_v.size
    assert isinstance(my_result.escore, float)