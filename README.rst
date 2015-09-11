XL-mHG
======

This is an efficient Python/Cython implementation of the nonparametric XL-mHG test for enrichment in ranked binary lists. The XL-mHG test is an extension of the mHG test, which was developed by `Dr. Zohar Yakhini <http://bioinfo.cs.technion.ac.il/people/zohar>`_ and colleagues.

If you use the XL-mHG in your research, please cite `Eden et al. (2007) <http://dx.doi.org/10.1371/journal.pcbi.0030039>`_ and `Wagner (2015) <http://dx.doi.org/10.1101/018705>`_.

Installation
------------

.. code-block:: bash

	$ pip install xlmhg

Usage
-----

.. code-block:: python

	import xlmhg
	n,s,pval = xlmhg.test(v,X,L)

Where ``v`` is a NumPy array of type \"np.uint8\" containing only zeros and ones, ``X``, and ``L`` are parameters, and the return values have the following meanings:

- ``n``: The threshold which the XL-mHG test statistic was based on.
- ``s``: The value of the XL-mHG test statistic
- ``pval``: The XL-mHG p-value associated with ``s``.

Background
----------

For a discussion of the statistical background and implementation of this test, please see my `Technical Report on arXiv <http://arxiv.org/abs/1507.07905>`_.

Copyright and License
---------------------

Copyright (c) 2015 Florian Wagner

::

  XL-mHG is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License, Version 3,
  as published by the Free Software Foundation.
  
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  
  You should have received a copy of the GNU General Public License
  along with this program. If not, see <http://www.gnu.org/licenses/>.
