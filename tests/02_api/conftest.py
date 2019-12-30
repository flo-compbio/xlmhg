# Copyright (c) 2016-2019 Florian Wagner
#
# This file is part of XL-mHG.

"""Fixtures for the `xlmhg` API tests."""

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


