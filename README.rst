XL-mHG
======

| |pypi| |versions| |license|

===========  ==================================
**master**   |travis-master| |codecov-master|
**develop**  |travis-develop| |codecov-develop|
===========  ==================================

This is an efficient Python/Cython implementation of the semiparametric
`XL-mHG test`__ for enrichment in ranked lists. The XL-mHG test is an extension
of the nonparametric `mHG test`__, which was developed by `Dr. Zohar
Yakhini`__ and colleagues.

__ xlmhg_paper_
__ mhg_paper_
__ zohar_

If you use the XL-mHG test in your research, please cite `Eden et al. (PLoS
Comput Biol, 2007)`__ and `Wagner (PLoS One, 2015)`__.

__ mhg_paper_
__ go_pca_paper_

Installation
------------

.. code-block:: bash

    $ pip install xlmhg

Usage
-----

.. code-block:: python

    import xlmhg
    stat, cutoff, pval = xlmhg.xlmhg_test(v, X, L)

Where: ``v`` is the ranked list of 0's and 1's, represented by a NumPy array of
type \"np.uint8\", `X`` and ``L`` are parameters, and the return values have
the following meanings:

- ``stat``: The XL-mHG test statistic
- ``cutoff``: The cutoff at which the XL-mHG test statistic was attained
- ``pval``: The XL-mHG p-value

What do the ``X`` and ``L`` parameters mean?
--------------------------------------------

- ``X`` refers to the minimum number of "1's" that have to be seen before
  anything can be called "enrichment".
- ``L`` is the lowest cutoff (i.e., the largest ``n``) that is being tested
  for enrichment.

A more direct way to understand ``X`` and ``L`` is through the definition of
the XL-mHG test statistic. It is defined as the minimum hypergeometric p-value
over all cutoffs at which at least ``X`` "1's" have already been seen, and
excluding any cutoffs larger than ``L``. For `X=1` and `L=N`, the XL-mHG test
reduces to the mHG test.

Background
----------

For a discussion of the statistical background and implementation of this test,
please see the `Technical Report on arXiv <http://arxiv.org/abs/1507.07905>`_,
as well as the `XL-mHG PeerJ Preprint article`__.

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


.. _xlmhg_paper: https://doi.org/10.7287/peerj.preprints.1962v1

.. _zohar: http://bioinfo.cs.technion.ac.il/people/zohar

.. _mhg_paper: https://dx.doi.org/10.1371/journal.pcbi.0030039

.. _go_pca_paper: https://dx.doi.org/10.1371/journal.pone.0143196

.. |pypi| image:: https://img.shields.io/pypi/v/xlmhg.svg
    :target: https://pypi.python.org/pypi/xlmhg
    :alt: PyPI version

.. |versions| image:: https://img.shields.io/pypi/pyversions/xlmhg.svg
    :target: https://pypi.python.org/pypi/xlmhg
    :alt: Python versions supported

.. |license| image:: https://img.shields.io/pypi/l/xlmhg.svg
    :target: https://pypi.python.org/pypi/xlmhg
    :alt: License

.. |travis-master| image:: https://travis-ci.org/flo-compbio/xlmhg.svg?branch=master
    :alt: Build Status (master branch)
    :scale: 100%
    :target: https://travis-ci.org/flo-compbio/xlmhg.svg?branch=master

.. |travis-develop| image:: https://travis-ci.org/flo-compbio/xlmhg.svg?branch=develop
    :alt: Build Status (develop branch)
    :scale: 100%
    :target: https://travis-ci.org/flo-compbio/xlmhg.svg?branch=develop

.. |codecov-master| image:: https://codecov.io/gh/flo-compbio/xlmhg/branch/master/graph/badge.svg
    :alt: Coverage (master branch)
    :target: https://codecov.io/gh/flo-compbio/xlmhg/branch/master

.. |codecov-develop| image:: https://codecov.io/gh/flo-compbio/xlmhg/branch/develop/graph/badge.svg
    :alt: Coverage (develop branch)
    :target: https://codecov.io/gh/flo-compbio/xlmhg/branch/develop
