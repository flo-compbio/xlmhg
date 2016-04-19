XL-mHG
======

===========  ================
**master**   |travis-master|
**develop**  |travis-develop|
===========  ================

This is an efficient Python/Cython implementation of the semiparametric
`XL-mHG test`__ for enrichment in ranked lists with boolean (0/1-valued)
entries. The XL-mHG test is an extension of the nonparametric `mHG test`__,
which was developed by `Dr. Zohar Yakhini`__ and colleagues.

__ xlmhg_paper_
__ mhg_paper_
__ zohar_

If you use the XL-mHG test in your research, please cite `Eden et al. (PLoS
Comput Biol, 2007)`__ and `Wagner (PeerJ Preprints, 2016)`__.

__ mhg_paper_
__ xlmhg_paper_

Installation
------------

.. code-block:: bash

    $ pip install xlmhg

Usage
-----

.. code-block:: python

    import xlmhg
    stat, n_star, pval = xlmhg.xlmhg_test(v, X, L)

Where ``v`` is a NumPy array of type \"np.uint8\" containing only zeros and ones, ``X``, and ``L`` are parameters, and the return values have the following meanings:

- ``stat``: The XL-mHG test statistic
- ``n_star``: The cutoff at which the XL-mHG test statistic was attained
- ``pval``: The XL-mHG p-value

What do the ``X`` and ``L`` parameters mean?
--------------------------------------------

- ``X`` refers to the minimum number of "1's" that have to be seen before anything can be called "enrichment".
- ``L`` is the lowest cutoff (i.e., the largest ``n``) that is being tested for enrichment.

A more direct way to understand ``X`` and ``L`` is through the definition of the XL-mHG test statistic. It is defined as the minimum hypergeometric p-value over all cutoffs at which at least ``X`` "1's" have already been seen, and which are at or below the n'th cutoff. All other cutoffs are ignored. For `X=1` and `L=N`, no relevant cutoffs are ignored, and the XL-mHG test reduces to the mHG test.

Background
----------

For a discussion of the statistical background and implementation of this test, please see my `Technical Report on arXiv <http://arxiv.org/abs/1507.07905>`_, as well as my `PeerJ Preprint article`__.

__ xlmhg_paper_

Copyright and License
---------------------

Copyright (c) 2015, 2016 Florian Wagner

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


.. |travis-master| image:: https://travis-ci.org/flo-compbio/xlmhg.svg?branch=master
    :alt: Build Status (master branch)
    :scale: 100%
    :target: https://travis-ci.org/flo-compbio/xlmhg.svg?branch=master

.. |travis-develop| image:: https://travis-ci.org/flo-compbio/xlmhg.svg?branch=develop
    :alt: Build Status (develop branch)
    :scale: 100%
    :target: https://travis-ci.org/flo-compbio/xlmhg.svg?branch=develop

.. _xlmhg_paper: https://doi.org/10.7287/peerj.preprints.1962v1
.. _zohar: http://bioinfo.cs.technion.ac.il/people/zohar
.. _mhg_paper: https://dx.doi.org/10.1371/journal.pcbi.0030039