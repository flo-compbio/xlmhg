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

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import numpy as np
import pytest

from xlmhg import xlmhg_test

@pytest.fixture
def v():
    v = np.uint8([1, 0, 1, 1, 0, 1] + [0] * 12 + [1, 0])  # example from
    return v

def test_mhg(v):
    # test regular mHG test
    res = xlmhg_test(v)
    assert res[0] == 0.01393188854489164
    assert res[1] == 6
    assert res[2] == 0.0244453044375645

def test_O1bound(v):
    # test if we return the O(1)-bound if that's equal to or smaller than
    # pval_thresh
    res = xlmhg_test(v, pval_thresh=0.07)
    assert res[2] == 0.0696594427244582

def test_ONbound(v):
    # test if we return the O(N)-bound instead of calculating the p-value if
    # the bound is equal to or smaller than pval_thresh
    res = xlmhg_test(v, pval_thresh=0.045)
    assert res[2] == 0.04179566563467492

def test_lowerbound(v):
    # test if we return the O(1)-bound when stat > pval_thresh
    res = xlmhg_test(v, pval_thresh=0.01)
    assert res[2] == 0.0696594427244582

def test_X(v):
    # test effect of X
    res = xlmhg_test(v, X=4)
    assert res[2] == 0.01876934984520124

def test_L(v):
    res = xlmhg_test(v, L=6)
    assert res[2] == 0.019801341589267284

def test_skip(v):
    res = xlmhg_test(v, skip_pval=True)
    assert res[2] is None

