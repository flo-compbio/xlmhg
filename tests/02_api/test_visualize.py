# Copyright (c) 2016-2019 Florian Wagner
#
# This file is part of XL-mHG.

"""Tests the visualizing function of the Python API (`get_result_figure`)."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import str as text

import os

import pytest
import numpy as np
from plotly.offline import plot

import xlmhg

def test_figure(tmpdir):

    v = np.uint8([1,0,1,1,0,1] + [0]*12 + [1,0])
    X = 3
    L = 10

    N = v.size
    indices = np.uint16(np.nonzero(v)[0])

    result = xlmhg.get_xlmhg_test_result(N, indices, X=X, L=L)

    fig = xlmhg.get_result_figure(result)
    output_file = text(tmpdir.join('plot1.html'))
    plot(fig, filename=output_file, auto_open=False)
    assert os.path.isfile(output_file)

    fig = xlmhg.get_result_figure(result, width=500, height=350)
    output_file = text(tmpdir.join('plot2.html'))
    plot(fig, filename=output_file, auto_open=False)
    assert os.path.isfile(output_file)

    fig = xlmhg.get_result_figure(result, show_title=True, show_inset=False)
    output_file = text(tmpdir.join('plot3.html'))
    plot(fig, filename=output_file, auto_open=False)
    assert os.path.isfile(output_file)


def test_figure_double_axis(tmpdir):

    v = np.uint8([1,0,1,1,0,1] + [0]*12 + [1,0])
    X = 3
    L = 10

    N = v.size
    indices = np.uint16(np.nonzero(v)[0])

    result = xlmhg.get_xlmhg_test_result(N, indices, X=X, L=L)

    fig = xlmhg.get_result_figure(result, plot_fold_enrichment=True)
    output_file = text(tmpdir.join('plot4.html'))
    plot(fig, filename=output_file, auto_open=False)
    assert os.path.isfile(output_file)