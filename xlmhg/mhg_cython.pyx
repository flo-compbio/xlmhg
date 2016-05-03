# Copyright (c) 2015, 2016 Florian Wagner
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

#cython: profile=False, wraparound=False, boundscheck=False, cdivision=True

"""XL-mHG Cython implementation."""

DEF DEFAULT_TOL = 1e-12

cdef extern from "math.h":
    long double ABS "fabsl" (long double x)
    long double NAN "nanl" (const char* tagp)

cimport cython

import numpy as np
cimport numpy as np

np.import_array()


def get_default_tol():
    return float(DEFAULT_TOL)


cdef inline int is_equal(long double a, long double b, long double tol):
    # tests equality of two floating point numbers
    # (of type long doube => 80-bit extended precision)
    if a == b or (ABS(a-b) <= tol * max(ABS(a), ABS(b))):
        return 1
    else:
        return 0


cdef long double get_hgp(long double p, int k, int N, int K, int n):
    # calculates hypergeometric p-value when f(k | N,K,n) is already known
    cdef long double pval = p
    while k < min(K, n):
        p *= (<long double>((n-k)*(K-k)) /\
                <long double>((k+1)*(N-K-n+k+1)))
        pval += p
        k += 1
    return pval


def get_xlmhg_stat(unsigned short[::1] indices, int N, int K, int X, int L,
                   long double tol=DEFAULT_TOL):
    """Calculates the XL-mHG test statistic."""
    # special cases
    if K == 0 or K == N or K < X:
        return 1.0, 0

    cdef long double hgp
    cdef int cutoff = 0
    cdef long double stat = 1.1
    cdef int i = 0
    cdef int n = 0
    cdef int k = 0
    cdef long double p = 1.0
    while i < K and indices[i] < L:
        while n < indices[i]:
            # "add zeros"
            # calculate f(k; N,K,n+1) from f(k; N,K,n)
            p *= (<long double>((n+1)*(N-K-n+k)) /
                  <long double>((N-n)*(n-k+1)))
            n += 1
        # "add one" => calculate hypergeometric p-value
        # calculate f(k+1; N,K,n+1) from f(k; N,K,n)
        p *= (<long double>((n+1)*(K-k)) /\
                <long double>((N-n)*(k+1)))
        k += 1
        n += 1
        if k >= X: # calculate p-value only if enough elements have been seen
            hgp = get_hgp(p, k, N, K, n)
            if hgp < stat and is_equal(hgp, stat, tol) == 0:
                stat = hgp
                cutoff = n
        i += 1
    stat = min(stat, 1.0) # because we initially set stat to 1.1
    return stat, cutoff


def get_xlmhg_bound(int N, int K, int X, int L, long double stat,
                    long double tol=DEFAULT_TOL):
    """PVAL-BOUND: Calculate an upper bound for the XL-mHG p-value in O(N)."""
    # we assume that:
    # 0 < stat <= 1.0
    # 1 <= X <= N
    # 1 <= L <= N
    cdef int n, k, w, min_KL
    cdef int k_min, k_max
    cdef long double p, hgp

    if stat == 1.0:
        # by definition
        return 1.0
    elif X > K or X > L:
        # since X > 0, this includes the case K=0
        return 0.0

    min_KL = min(K, L)
    k_min = 0
    p = 1.0
    n = 1
    while (n <= K or (p <= stat or is_equal(p, stat, tol) != 0)) and n <= L:
        if n <= K:
            k = n
            p *= (<long double>(K-n+1) / <long double>(N-n+1))
            if k < X or (p > stat and is_equal(p, stat, tol) == 0):
                # we're not in R yet => set k_min
                k_min = n
                # remember to later do k_min += 1
                # (since we're interested in the first k that reaches R)
        else:
            k = K
            p *= (<long double>n / <long double>(n-K))

        n += 1

    if k_min == min_KL:
        # R is empty
        return 0.0

    # R is not empty! Next, we we need to know if R ended before we reached L.
    
    k_min += 1    
    # if n <= L, we know that we left R
    # if n == L+1, we need to check whether the previously calculated p-value was in R or not
    if n <= L or (n == L+1 and p > stat and is_equal(p, stat, tol) == 0):
        # yes => k_max = K
        return min((K-k_min+1)*stat, 1.0)
    
    # We did not leave R. Next, we need to try to "go down the diagonal", until we step out of R.
    n -= 1
    k = min(n, K)
    hgp = p
    #print('Test (X=%d,L=%d,stat=%.3e):' %(X, L, stat), p, k, n-k)
    while hgp <= stat or is_equal(hgp, stat, tol) != 0:
        p *= (<long double>(k*(N-K-n+k)) / <long double>((n-k+1)*(K-k+1)))
        hgp += p
        k -= 1
        
    # now we left R
    k_max = k+1
    
    return min((k_max-k_min+1)*stat, 1.0)


def get_xlmhg_pval1(int N, int K, int X, int L, long double stat, \
                    long double[:,::1] table, long double tol=DEFAULT_TOL):
    """PVAL1: Calculate the XL-mHG p-value in O(N^2)."""

    # cheap checks
    if stat == 1.0:
        return 1.0
    elif stat == 0:
        return 0.0
    elif K == 0 or K == N or K < X:
        return 0.0

    # initialization
    cdef int W, n, k, w
    cdef long double p_start, p, hgp

    W = N-K
    table[0,0] = 1.0
    p_start = 1.0
    # go over all cutoffs
    for n in range(1, N+1):

        if K >= n:
            k = n
            p_start *= ((<long double>(K-n+1)) /\
                    (<long double>(N-n+1)))
        else:
            k = K
            p_start *= ((<long double>n) /\
                    <long double>(n-K))

        if p_start <= 0.0:
            # not enough floating point precision to calculate p-value
            #return <long double>(float('nan'))
            return NAN("")

        p = p_start
        hgp = p
        w = n - k

        # R is the space of configurations with mHG better than or equal to the
        # one observed
        # - go over all configurations for threshold n
        # - start with highest possible enrichment and then go down
        # - as long as we're in R, all paths going through this configuration
        #   are "doomed"
        # - because we're using (K x W) grid instead of parallelogram,
        #   "going down" becomes going down and right...

        # no configuration with threshold > L or threshold < X can be in R 
        if n <= L and n >= X:
            # find the first configuration that's not in R
            # this happens when either k < X, or hypergeometric p-value > mHG
            # if k == 0 or w == W, we have hypergeometric p-value = 1
            # since mHG < 1, as soon as k == 0 or w == W, we have left R
            while k >= X and w < W and (hgp < stat or is_equal(hgp, stat, tol)):
                # k > 0 is implied
                table[k, w] = 0 # we're still in R
                p *= ((<long double>(k*(N-K-n+k))) / (<long double>((n-k+1)*(K-k+1))))
                hgp += p
                w += 1
                k -= 1

        # fill in rest of the table based on entries for cutoff n-1
        while k >= 0 and w <= W:
            if w > 0 and k > 0:
                table[k, w] = \
                    table[k, w-1] * (<long double>(W-w+1) / <long double>(N-n+1)) + \
                    table[k-1, w] * (<long double>(K-k+1) / <long double>(N-n+1))
            elif w > 0:
                table[k, w] = \
                    table[k, w-1] * (<long double>(W-w+1) / <long double>(N-n+1))
            elif k > 0:
                table[k, w] = \
                    table[k-1, w] * (<long double>(K-k+1) / <long double>(N-n+1))
            w += 1
            k -= 1

    return 1.0 - table[K, W]

def get_xlmhg_pval2(int N, int K, int X, int L, long double stat,\
                    long double[:,::1] table, long double tol=DEFAULT_TOL):
    """PVAL2: Improved calculation of the XL-mHG p-value in O(N^2)."""

    # cheap checks
    if stat == 1.0:
        return 1.0
    elif stat == 0:
        return 0.0
    elif K == 0 or K == N or K < X:
        return 0.0

    # initialization
    cdef int W, n, k, w
    cdef long double pval, p_start, p, hgp

    # go over the first L cutoffs
    pval = 0.0
    W = N-K
    table[0,0] = 1.0
    p_start = 1.0
    for n in range(1, L+1):

        if K >= n:
            k = n
            p_start *= ((<long double>(K-n+1)) /\
                    (<long double>(N-n+1)))
        else:
            k = K
            p_start *= ((<long double>n) /\
                    <long double>(n-K))

        if p_start <= 0.0:
            # not enough floating point precision to calculate p-value
            return NAN("")

        p = p_start
        hgp = p
        w = n - k

        if k == K and (hgp > stat and not is_equal(hgp, stat, tol)):
            # We've exited R (or we were never in it).
            # That means we're done here!
            break

        # R is the space of configurations with mHG better than or equal to the
        # one observed
        # - go over all configurations for threshold n
        # - start with highest possible enrichment and then go down
        # - as long as we're in R, all paths going through this configuration
        #   are "doomed"
        # - because we're using (K x W) grid instead of parallelogram,
        #   "going down" becomes going down and right...

        # find the first configuration that's not in R
        # this happens when either k < X, or hypergeometric p-value > mHG
        # if k == 0 or w == W, we have hypergeometric p-value = 1
        # since mHG < 1, as soon as k == 0 or w == W, we have left R
        while k >= X and w < W and \
                (hgp < stat or is_equal(hgp, stat, tol)):
            # we're still in R
            table[k, w] = 0.0

            # check if we've "just entered" R (this is only possible "from below")
            if table[k-1, w] > 0.0:
                # calculate the fraction of "fresh" paths (paths which have never entered R before)
                # that enter here, and add that number to r
                pval += (table[k-1, w] * (<long double>(K-k+1)/<long double>(N-n+1)))
 

            p *= ((<long double>(k*(N-K-n+k))) / (<long double>((n-k+1)*(K-k+1))))
            hgp += p
            w += 1
            k -= 1

        # fill in rest of the table based on entries for cutoff n-1
        while k >= 0 and w <= W:
            if k == 0:
                # paths only come in "from the left"
                table[k, w] = \
                    table[k, w-1] * (<long double>(W-w+1) / <long double>(N-n+1))
            elif w == 0:
                # paths only come in "from below"
                table[k, w] = \
                    table[k-1, w] * (<long double>(K-k+1) / <long double>(N-n+1))
            else:
                # paths come in "from the left" and "from below"
                table[k, w] = \
                    table[k, w-1] * (<long double>(W-w+1) / <long double>(N-n+1)) + \
                    table[k-1, w] * (<long double>(K-k+1) / <long double>(N-n+1))
            w += 1
            k -= 1

    return pval


def get_xlmhg_escore(unsigned short[::1] indices, int N, int K, int X, int L,
                     long double hg_pval_thresh,
                     long double tol=DEFAULT_TOL):
    """ESCORE: Calculate the XL-mHG E-score in O(N)."""
    # special cases
    if K == 0 or K == N or K < X:
        return float('nan')

    cdef long double hgp
    cdef long double e
    cdef long double escore = 0.0
    cdef int i = 0
    cdef int n = 0
    cdef int k = 0
    cdef long double p = 1.0
    while i < K and indices[i] < L:
        while n < indices[i]:
            # "add zeros"
            # calculate f(k; N,K,n+1) from f(k; N,K,n)
            p *= (<long double>((n+1)*(N-K-n+k)) /
                  <long double>((N-n)*(n-k+1)))
            n += 1
        # "add one" => calculate hypergeometric p-value
        # calculate f(k+1; N,K,n+1) from f(k; N,K,n)
        p *= (<long double>((n+1)*(K-k)) /\
                <long double>((N-n)*(k+1)))
        k += 1
        n += 1
        if k >= X: # calculate E-score only if enough elements have been seen
            e = <long double>k / (<long double>(n*K) / <long double>N)
            # only calculate p-value if e(n) is larger than current E-score
            if e > escore and is_equal(e, escore, tol) == 0:
                hgp = get_hgp(p, k, N, K, n)
                # check if hypergeometric p-value meets thresholds crit.
                if hgp <= hg_pval_thresh or \
                        is_equal(hgp, hg_pval_thresh, tol) != 0:
                    escore = e
        i += 1
    if escore == 0.0:
        escore = NAN("")
    return escore
