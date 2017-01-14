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

"""Python API for visualizing XL-mHG test results."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
_oldstr = str
from builtins import *

from math import floor, ceil
# from collections import Iterable

import numpy as np
import plotly.graph_objs as go

import xlmhg
from xlmhg import mHGResult
from xlmhg.mhg import get_hgp, is_equal


def get_hypergeometric_stats(N, indices):
    """Calculates hypergeom. p-values and fold enrichments for all cutoffs.

    Parameters
    ----------
    N: int
        The length of the list
    indices:  `numpy.ndarray` with ``dtype=np.uint16``
        The (sorted) indices of the "1's" in the list.
    """
    assert isinstance(N, (int, np.integer))
    assert isinstance(indices, np.ndarray) and \
            np.issubdtype(indices.dtype, np.uint16)

    K = indices.size

    pvals = np.empty(N+1, dtype=np.float64)
    folds = np.empty(N+1, dtype=np.float64)
    pvals[0] = 1.0
    folds[0] = 1.0

    n = 0
    k = 0
    p = 1.0
    while n < N:
        if k < K and indices[k] == n:
            # "add one"
            # calculate f(k+1; N,K,n+1) from f(k; N,K,n)
            p *= (float((n+1) * (K-k)) / \
                  float((N-n) * (k+1)))
            k += 1
        else:
            # "add zero"
            # calculate f(k; N,K,n+1) from f(k; N,K,n)
            p *= (float((n+1) * (N-K-n+k)) /
                  float((N-n) * (n-k+1)))
        n += 1
        # calculate hypergeometric p-value
        pvals[n] = get_hgp(p, k, N, K, n)
        # calculate fold enrichment
        folds[n] = k / (K*(n/float(N)))

    return pvals, folds


def get_result_figure(
        result, show_title=False, title=None, show_inset=True,
        plot_fold_enrichment=False,
        width=800, height=350, font_size=24, margin=None,
        font_family='Computer Modern Roman, serif',
        score_color='rgb(0,109,219)',
        enrichment_color='rgb(219,109,0)',
        cutoff_color='rgba(255, 109, 182,0.5)',
        line_width=2.0):
    """Visualize an XL-mHG test result.

    Parameters
    ----------
    result : `mHGResult`
        The test result.
    show_title : bool, optional
        Whether to include a title in the figure. If `title` is not
        ``None``, this parameter is ignored. [False]
    title : str or None, optional
        Figure title. If not ``None``, `show_title` is ignored. [None]
    show_inset : bool, optional
        Whether to show test parameters and p-value as an inset. [True]
    plot_fold_enrichment : bool, optional
        Whether to plot the fold enrichment on a second axis. [False]
    width : int, optional
        The width of the figure (in pixels). [800]
    height : int, optional
        The height of the figure (in pixels). [350]
    font_size : int, optional
        The font size to use. [20]
    margin : dict, optional
        A dictionary specifying the figure margins (in pixels).
        Valid keys are "l" (left), "r" (right), "t" (top), and "b" (bottom).
        Missing keys are replaced by Plotly default values. If ``None``, will
        be set to a dictionary specifying a left margin of 100 px, and a top
        margin of 40 px. [None]
    font_family : str, optional
        The font family (name) to use. ["Computer Modern Roman, serif"]
    score_color : str, optional
        The color used for plotting the enrichment scores. ["rgb(0,109,219)"]
    enrichment_color : str, optional
        The color used for plotting the fold enrichment values (if enabled).
        ["rgb(219,109,0)"]
    cutoff_color : str, optional
        The color used for indicating the XL-mHG test cutoff.
        ["rgba(255, 109,182,0.5)"]
    line_width : int or float, optional
        The line width used for plotting. [2.0]

    Returns
    -------
    `plotly.graph_obs.Figure`
        The Plotly figure.
    """

    assert isinstance(result, mHGResult)
    assert isinstance(show_title, bool)
    if title is not None:
        assert isinstance(title, (str, _oldstr))
    assert isinstance(show_inset, bool)
    assert isinstance(plot_fold_enrichment, bool)
    assert isinstance(font_family, (str, _oldstr))
    assert isinstance(width, int)
    assert isinstance(height, int)
    assert isinstance(font_size, (int, float))
    if margin is not None:
        assert isinstance(margin, dict)
    assert isinstance(score_color, (str, _oldstr))
    assert isinstance(enrichment_color, (str, _oldstr))
    assert isinstance(line_width, (int, float))

    pvals, folds = get_hypergeometric_stats(result.N, result.indices)
    pval_max = max(int(ceil(-np.log10(np.amin(pvals)))), 1.0)
    pval_min = 0.0
    X = result.X
    L = result.L
    N = result.N
    K = result.K
    fold_start = result.indices[0] + 1

    data = []

    # generate p-value trace
    data.append(go.Scatter(
        x=np.arange(N+1),
        y=-np.log10(pvals),
        mode='line',
        line=dict(
            color=score_color,
            width=line_width,
        ),
        name='Enrichment score'
    ))

    # generate p-value axis
    tick_color = None
    if plot_fold_enrichment:
        tick_color = score_color
    yaxis = go.YAxis(
        #title='-log<sub>10</sub>(hypergeom. p-value)',
        title='Enrichment score',
        tickfont=dict(
            color=tick_color,
        ),
        autorange=False,
        #range=[pval_min, pval_max],
        range=[pval_min, pval_max],
        showgrid=False,
        #zeroline=False,
        zeroline=False,
        showline=True,
        domain=[0.15, 1.0],
        #mirror=True,
    )

    # additional y axis at the the bottom,
    # showing the occurrences of the "1's"
    yaxis3 = go.YAxis(
        domain=[0, 0.1],
        anchor='x',
        mirror=True,
        zeroline=False,
        showline=False,
        showgrid=False,
        autorange=False,
        range=[0, 1],
        ticks='',
        showticklabels=False,
    )

    # format p-value string
    pval_str = '%.1e' % (result.pval)
    e_idx = pval_str.index('e')
    exponent = int(pval_str[(e_idx + 1):])
    pval_str = pval_str[:e_idx] + '*10<sup>%d</sup>' % exponent

    # fe_str = '%.1fx' % (result.fold_enrichment)

    # if show_title:
    if show_title and title is None:
        title = 'XL-mHG test result (N=%d, K=%d)' % (N, K)

    # specify margins (if not provided)
    if margin is None:
        t = 42
        if title is None:
            t = 22
        margin = dict(
            l=80,
            t=t,
            b=75,
        )

    if plot_fold_enrichment:
        fold_min_int = -0.3
        if np.log2(np.amin(folds[fold_start:])) < -0.3:
            fold_min_int = int(floor(np.log2(np.amin(folds[fold_start:]))))
        fold_max_int = max(int(ceil(np.log2(np.amax(folds)))), 2)

        # generate fold enrichment trace
        data.append(go.Scatter(
            x=np.arange(fold_start, result.N + 1),
            y=np.log2(folds[fold_start:]),
            yaxis='y2',
            mode='line',
            line=dict(
                color=enrichment_color,
                width=line_width
            ),
        ))

        # generate fold enrichment axis
        yaxis2 = go.YAxis(
            title='log<sub>2</sub>(Fold enrichment)',
            # titlefont=dict(
            #    color='rgb(148, 103, 189)'
            # ),
            tickfont=dict(
                color=enrichment_color,
            ),
            range=[fold_min_int, fold_max_int],
            overlaying='y',
            side='right',
            showgrid=False,
            zeroline=False,
            showline=True,
        )

    font = dict(
        size=font_size,
        family=font_family,
    )

    # rectangles showing which ranks are excluded
    # in the calculation of the test statistic
    # (due to X and L parameters)
    rect_col = 'rgba(60,60,60,0.10)'
    rect1 = {
        'type': 'rect',
        'x0': 0,
        'y0': pval_min,
        'x1': result.indices[result.X-1] + 0.5,
        'y1': pval_max,
        'line': dict(
            width=0,
        ),
        'fillcolor': rect_col,
    }
    rect2 = {
        'type': 'rect',
        'x0': L+0.5,
        'y0': pval_min,
        'x1': N,
        'y1': pval_max,
        'line': dict(
            width=0,
        ),
        'fillcolor': rect_col,
    }

    # bars in second Y axis symbolizing the occurrences of the "1's"
    bars = []
    for n in result.indices:
        bars.append(dict(
            type='line',
            x0=n+1.0,
            y0=0.0,
            x1=n+1.0,
            y1=1.0,
            line=dict(
                color='black',
                width=line_width,
            ),
            yref='y3',
            opacity=0.7,
        ))

    annotations = []
    if show_inset:
        annotations.append(
            go.Annotation(
                x=0.95,
                y=0.95,
                align='right',
                showarrow=False,
                #text='X=%d, L=%d<br><b><i>p</i> = %s</b>' \
                #     % (result.X, result.L, pval_str),
                #text='%d/%d @ %d<br><b><i>p</i> = %s</b>' \
                #     % (result.k, result.K, result.cutoff, pval_str),
                text='<b><i>p</i> = %s</b><br>(%d/%d @ %d)' \
                     % (pval_str, result.k, result.K, result.cutoff),
                xref='paper',
                yref='paper',
                xanchor='right',
                yanchor='top',
                font=font,
            ),
        )

    line = {
        'type': 'line',
        'x0': result.cutoff,
        'y0': pval_min,
        'x1': result.cutoff,
        'y1': pval_max,
        'line': dict(
            color=cutoff_color,
            width=line_width,
            dash='dash',
        ),
    }

    line2 = {
        'type': 'line',
        'x0': 0,
        'y0': 0,
        'x1': result.N,
        'y1': 0,
        'line': dict(
            color='black',
            width=1.0,
        ),
    }

    layout = go.Layout(
        width=width,
        height=height,
        margin=margin,
        xaxis=dict(
            title='Rank cutoff',
            zeroline=False,
            range=[1.0, result.N],
            showline=True,
            anchor='y3',
        ),
        yaxis=yaxis,
        yaxis3=yaxis3,
        titlefont=dict(
            size=font_size,
            family=font_family,
        ),
        font=dict(
            size=font_size,
            family=font_family,
        ),
        showlegend=False,
        shapes=[
            rect1,
            rect2,
            line,
            line2,
        ] + bars,
        title=title,
        annotations=annotations,
    )

    if plot_fold_enrichment:
        layout.yaxis2 = yaxis2

    fig = go.Figure(
        data=data,
        layout=layout,
    )

    return fig
