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

"""Tests for the simple Python API (`xlmhg_test`)."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import str as text

import numpy as np
import pytest

from xlmhg import mHGResult, xlmhg_test, get_xlmhg_test_result

@pytest.fixture
def my_indices(my_v):
    indices = np.uint16(np.nonzero(my_v)[0])
    return indices


def test_mhg(my_v):
    # test regular mHG test
    res = xlmhg_test(my_v)
    assert res[0] == 0.01393188854489164
    assert res[1] == 6
    assert res[2] == 0.0244453044375645


def test_X(my_v):
    # test effect of X
    res = xlmhg_test(my_v, X=4)
    assert res[2] == 0.01876934984520124


def test_L(my_v):
    res = xlmhg_test(my_v, L=6)
    assert res[2] == 0.019801341589267284


def test_result(my_ind, my_v):
    N = my_v.size
    result = get_xlmhg_test_result(N, my_ind)
    assert isinstance(result, mHGResult)


def test_limit_stat(my_incredible_stat_v):
    res = xlmhg_test(my_incredible_stat_v)
    assert res[0] == 0.0
    assert res[1] == 500
    assert res[2] == 0.0


def test_list_too_long(my_much_too_long_v):
    with pytest.raises(ValueError):
        result = xlmhg_test(my_much_too_long_v)


def test_table_too_small(my_N, my_ind, my_v):
    K = my_ind.size
    with pytest.raises(ValueError):
        table = np.empty(((my_N-K), (my_N-K)), np.longdouble)
        result = xlmhg_test(my_v, table=table)


