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

"""Fixtures for the `xlmhg` API tests."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import str as text

import numpy as np
import pytest

# from xlmhg import mHGResult, xlmhg_test, get_xlmhg_test_result

@pytest.fixture
def my_v():
    v = np.uint8([1, 0, 1, 1, 0, 1] + [0] * 12 + [1, 0])  # example from paper
    return v

@pytest.fixture
def my_N(my_v):
    return my_v.size


@pytest.fixture
def my_ind(my_v):
    return np.uint16(np.nonzero(my_v)[0])


@pytest.fixture
def my_much_too_long_v():
    v = np.uint8([1, 0, 1, 1, 0, 1] + [0] * 100000)
    return v


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


