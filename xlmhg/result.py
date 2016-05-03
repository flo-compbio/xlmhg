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

"""Contains the `mHGResult` class."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import hashlib
import logging

import numpy as np

from . import mhg_cython

logger = logging.getLogger(__name__)


class mHGResult(object):
    """The result of performing an XL-mHG test.

    """
    def __init__(self, N, indices, X, L, stat, cutoff, pval,
                 pval_thresh=None, escore_pval_thresh=None, escore_tol=None):

        assert isinstance(N, int)
        assert isinstance(indices, np.ndarray) and indices.ndim == 1 and \
               np.issubdtype(indices.dtype, np.uint16) and \
               indices.flags.c_contiguous
        assert isinstance(X, int)
        assert isinstance(L, int)
        assert isinstance(stat, float)
        assert isinstance(cutoff, int)
        assert isinstance(pval, float)
        if pval_thresh is not None:
            assert isinstance(pval_thresh, float)
        if escore_pval_thresh is not None:
            assert isinstance(escore_pval_thresh, float)
        if escore_tol is not None:
            assert isinstance(escore_tol, float)

        self.indices = indices
        self.N = N
        self.X = X
        self.L = L
        self.stat = stat
        self.cutoff = cutoff
        self.pval = pval
        self.pval_thresh = pval_thresh
        self.escore_pval_thresh = escore_pval_thresh
        self.escore_tol = escore_tol

    def __repr__(self):
        return '<%s object (N=%d, K=%d, pval=%.1e, hash="%s")>' \
               % (self.__class__.__name__,
                  self.N, self.K, self.pval, self.hash)

    def __str__(self):
        return '<%s object (N=%d, K=%d, X=%d, L=%d, pval=%.1e)>' \
               % (self.__class__.__name__,
                  self.N, self.K, self.X, self.L, self.pval)

    def __eq__(self, other):
        if self is other:
            return True
        elif type(self) == type(other):
            return self.hash == other.hash
        else:
            return NotImplemented

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def v(self):
        v = np.zeros(self.N, dtype=np.uint8)
        v[self.indices] = 1
        return v

    @property
    def K(self):
        return self.indices.size

    @property
    def k(self):
        return int(np.sum(self.indices < self.cutoff))

    @property
    def hash(self):
        data_str = ';'.join(
            [str(repr(var)) for var in
             [self.N, self.K, self.X, self.L,
              self.stat, self.cutoff, self.pval,
              self.pval_thresh, self.escore_pval_thresh]])
        data_str += ';'
        data = data_str.encode('UTF-8') + self.indices.tobytes()
        return str(hashlib.md5(data).hexdigest())

    @property
    def escore(self):
        hg_pval_thresh = self.escore_pval_thresh or self.pval
        escore_tol = self.escore_tol or mhg_cython.get_default_tol()
        es = mhg_cython.get_xlmhg_escore(
            self.indices, self.N, self.K, self. X, self.L,
            hg_pval_thresh, escore_tol)
        return es
