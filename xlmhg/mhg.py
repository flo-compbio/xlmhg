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

"""XL-mHG Python implementation."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import numpy as np

DEFAULT_TOL = 1e-12


def is_equal(a, b, tol):
    """Ratio test to check if two floating point numbers are equal.

    Parameters
    ----------
    a: float
        The first floating point number.
    b: float
        The second floating point number.
    tol: float
        The tolerance used.

    Returns
    -------
    bool
        Whether or not the two numbers are deemed equal.
    """
    if a == b or abs(a-b) <= tol * max(abs(a), abs(b)):
        return True
    else:
        return False

def get_hgp(p, k, N, K, n):
    """Calculate the hypergeometric p-value when p = f(k; N,K,n) is already known.
    """
    pval = p
    while k < min(K, n):
        p *= (float((n-k)*(K-k) / float((k+1)*(N-K-n+k+1))))
        pval += p
        k += 1
    return pval

def get_xlmhg_stat(v, X, L, tol=DEFAULT_TOL):
    """Calculate the XL-mHG test statistic using recurrence relations.
    
    Parameters
    ----------
    v: np.ndarray with dtype=np.uint8
        The ranked list.
    X: int
        The XL-mHG ``X`` parameter.
    L: int
        The XL-mHG ``L`` parameter.
    tol: float, optional
        The tolerance used for comparing floats. [1e-12]
    
    Returns
    -------
    s: float
        The XL-mHG test statistic.
    n_star: int
        The (first) cutoff at which s was attained.
    """
    assert isinstance(v, np.ndarray) and v.ndim == 1 and \
           np.issubdtype(v.dtype, np.integer)
    assert isinstance(X, int)
    assert isinstance(L, int)
    assert isinstance(tol, float)

    N = v.size
    if not N > 0:
        raise ValueError('List is empty!')
    if not (1 <= X <= N):
        raise ValueError(
            'Invalid value X=%d; should be >= 1 and <= %d.' % (X, N)
        )
    if not (1 <= L <= N):
        raise ValueError(
            'Invalid value L=%d; should be >= 1 and <= %d.' % (L, N)
        )
    if not (0.0 <= tol < 1.0):
        raise ValueError('Invalid value tol=%.1e; should be in [0,1)' % (tol))
    
    K = int(np.sum(v != 0))
    if K == 0:
        return 1.0, 0
 
    p = 1.0
    stat = 1.1
    n_star = 0
    k = 0
    for n in range(L):
        if v[n] == 0:
            # calculate f(k; N,K,n+1) from f(k; N,K,n)
            p *= (float((n+1)*(N-K-n+k)) / float((N-n)*(n-k+1)))
        else:
            # we hit a 1
            # calculate f(k+1; N,K,n+1) from f(k; N,K,n)
            p *= (float((n+1)*(K-k)) / float((N-n)*(k+1)))
            k += 1
            # calculate hypergeometric p-value only if enough elements have
            # been seen
            if k >= X:
                hgp = get_hgp(p, k, N, K, n+1)
                if hgp < stat and not is_equal(hgp, stat, tol):
                    stat = hgp
                    n_star = n+1

    stat = min(stat, 1.0)
    return stat, n_star

def get_xlmhg_pval1(N, K, X, L, stat, tol=DEFAULT_TOL):
    """Calculate the XL-mHG p-value using "Algorithm 1".

    Parameters
    ----------
    N: int
        The length of the list.
    K: int
        The number of 1's in the list.
    X: int
        The XL-mHG ``X`` parameter.
    L: int
        The XL-mHG ``L`` parameter.
    stat: float
        The XL-mHG test statistic.
    tol: float, optional
        The tolerance used for comparing floats. [1e-12]

    Returns
    -------
    float
        The XL-mHG p-value. NaN if floating point precision was insufficient
        for calculating the p-value.
    """
    # type checking
    assert isinstance(N, int)
    assert isinstance(X, int)
    assert isinstance(L, int)
    assert isinstance(stat, float)
    assert isinstance(tol, float)

    # raise exceptions for invalid parameters
    if not (N >= 1):
        raise ValueError('Invalid value N=%d; should be >= 1.' % (N))
    if not (1 <= X <= N):
        raise ValueError(
            'Invalid value X=%d; should be >= 1 and <= %d.' % (X, N)
        )
    if not (1 <= L <= N):
        raise ValueError(
            'Invalid value L=%d; should be >= 1 and <= %d.' % (L, N)
        )
    if not (0 < stat <= 1.0):
        raise ValueError(
            'Invalid value stat=%.1e; should be in (0;1].' % (stat,)
        )
    if not (0.0 <= tol < 1.0):
        raise ValueError('Invalid value tol=%.1e; should be in [0,1)' % (tol))

    # special case: stat = 1.0 => pval = 1.0
    if stat == 1.0:
        return 1.0
        
    found_R = False
    p_start = 1.0
    p = None
    hgp = None

    # fill dynamic programming table by going over all cutoffs n
    W = N-K
    table = np.empty((K+1, W+1), dtype=np.float64)
    table[0,0] = 1.0
    for n in range(1, N+1):
        
        if K >= n:
            k = n
            p_start *= (float(K-n+1) / float(N-n+1))
    
        else:
            k = K
            p_start *= (float(n) / float(n-K))
            
        if p_start == 0.0:
            # not enough floating point accuracy to calculate the
            # hypergeometric p-value
            return float('nan')

        p = p_start
        hgp = p
        w = n - k
        
        # no configuration with n > L or n < X can be in R
        if n <= L and n >= X:
            while k >= X and w < W and \
                    (hgp < stat or is_equal(hgp, stat, tol)):
                # we're still in R
                found_R = True
                table[k, w] = 0.0 # !
                p *= (float(k*(N-K-n+k)) / float((n-k+1)*(K-k+1)))
                hgp += p
                w += 1
                k -= 1
                
        # fill in rest of the table based on entries for cutoff n-1
        while k >= 0 and w <= W:
            if k > 0 and w > 0:
                table[k, w] = table[k, w-1] * (float(W-w+1)/float(N-n+1)) + \
                        table[k-1, w] * (float(K-k+1)/float(N-n+1))
            elif k > 0:
                table[k, w] = table[k-1, w] * (float(K-k+1)/float(N-n+1))
            elif w > 0:
                table[k, w] = table[k, w-1] * (float(W-w+1)/float(N-n+1))
            w += 1
            k -= 1
            
    if found_R:
        pval = 1.0 - table[K, W]
        if pval < 0.0:
            # insufficient floating point accuracy, set p-value to NaN
            pval = float('nan')
    else:
        # we've never encountered R => set p-value to 0
        pval = 0.0         

    return pval


def get_xlmhg_pval2(N, K, X, L, stat, tol=DEFAULT_TOL):
    """Calculate the XL-mHG p-value using "Algorithm 2".

    Parameters
    ----------
    N: int
        The length of the list.
    K: int
        The number of 1's in the list.
    X: int
        The XL-mHG ``X`` parameter.
    L: int
        The XL-mHG ``L`` parameter.
    stat: float
        The XL-mHG test statistic.
    tol: float, optional
        The tolerance used for comparing floats. [1e-12]

    Returns
    -------
    float
        The XL-mHG p-value. NaN if floating point precision was insufficient
        for calculating the p-value.
    """
    # type checking
    assert isinstance(N, int)
    assert isinstance(X, int)
    assert isinstance(L, int)
    assert isinstance(stat, float)
    assert isinstance(tol, float)

    # raise exceptions for invalid parameters
    if not (N >= 1):
        raise ValueError('Invalid value N=%d; must be >= 1.' %(N))
    if not (1 <= X <= N):
        raise ValueError(
            'Invalid value X=%d; must be >= 1 and <= %d.' %(X, N)
        )
    if not (1 <= L <= N):
        raise ValueError(
            'Invalid value L=%d; must be >= 1 and <= %d.' %(L, N)
        )
    if not (0 < stat <= 1.0):
        raise ValueError(
            'Invalid value s=%.1e; must be in (0,1].' %(stat)
        )
    if not (0.0 <= tol < 1.0):
        raise ValueError('Invalid value tol=%.1e; must be in [0,1)' %(tol))

    # special case: stat = 1.0 => pval = 1.0
    if stat == 1.0:
        return 1.0

    W = N-K
    table = np.empty((K+1, L+1), dtype=np.float64)
    table[0,0] = 1.0 # initially, *all* paths have never entered R before
    
    pval = 0.0
    p_start = 1.0
    p = None
    hgp = None
    k = None
    w = None

    # fill dynamic programming table and calculate XL-mHG p-value
    # note: we only need to go over the first L cutoffs, since lower cutoffs
    #       cannot be in R (by definition)
    for n in range(1, L+1):
        
        if K >= n:
            k = n
            p_start *= (float(K-n+1) / float(N-n+1))
        else:
            k = K
            p_start *= (float(n) / float(n-K))

        if p_start == 0.0:
            # not enough floating point precision to calculate
            # the hypergeometric p-value
            return float('nan')

        p = p_start
        hgp = p
        w = n - k
        
        if k == K and (hgp > stat and not is_equal(hgp, stat, tol)):
            # We've exited R (or we were never in it).
            # That means we're done here!
            break
            
        # Check if we've reached R. If so, "go down the diagonal" until we exit R.
        # Three conditions:
        # 1. k >= X         // No configuration with k < X can be in R.
        # 2. w < W          // No configuration with w = W can be in R.
        # 3. pval <= s      // The basic criterion for being in R.
        while k >= X and w < W and (hgp < stat or is_equal(hgp, stat, tol)):
            # We're in R!
            # Note:
            #   For w = W, we always have hgp = 1.0. Since stat < 1.0,
            #   we could just assume that w < W. But this assumption might fail
            #   due to limited floating point accuracy.
            
            # First things first: set table[k, w] to 0 to indicate that this is
            # R territory.
            table[k, w] = 0
            
            # check if we've "just entered" R (this is only possible "from below")
            if table[k-1, w] > 0:
                # calculate the fraction of "fresh" paths (paths which have never entered R before)
                # that enter here, and add that number to r
                pval += (table[k-1, w] * (float(K-k+1)/float(N-n+1)))
                
            p *= (float(k*(N-K-n+k)) / float((n-k+1)*(K-k+1)))
            hgp += p
            w += 1
            k -= 1
            
        # now we're no longer in R
        while k >= 0 and w <= W:
            if k == 0:
                # paths only come in "from the left"
                table[k, w] = table[k, w-1] * (float(W-w+1)/float(N-n+1))
            elif w == 0:
                # paths only come in "from below"
                table[k, w] = table[k-1, w] * (float(K-k+1)/float(N-n+1))
            else:
                # paths come in "from the left" and "from below"
                table[k, w] = table[k, w-1] * (float(W-w+1)/float(N-n+1)) + \
                        table[k-1, w] * (float(K-k+1)/float(N-n+1))
            w += 1
            k -= 1
            
    return pval
