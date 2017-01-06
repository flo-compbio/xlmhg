XL-mHG
======

| |pypi| |versions| |license|

===========  ====================================================================
**master**   |codecov-master| |travis-master| |appveyor-master| |docs-latest|
**develop**  |codecov-develop| |travis-develop| |appveyor-develop| |docs-develop|
===========  ====================================================================

This is an efficient Python/Cython implementation of the semiparametric
`XL-mHG test`__ for enrichment in ranked lists. The XL-mHG test is an extension
of the nonparametric `mHG test`__, which was developed by `Dr. Zohar
Yakhini`__ and colleagues.

__ xlmhg_paper_
__ mhg_paper_
__ zohar_

Installation
------------

.. code-block:: bash

    $ pip install xlmhg

Getting started
---------------

The `xlmhg` package provides two functions (one simple and more more advanced)
for performing XL-mHG tests. These functions are documented in the
`User Manual`__. Here's a quick example using the "simple" test function:

.. code-block:: python

    import xlmhg
    stat, cutoff, pval = xlmhg.xlmhg_test(v, X, L)

Where: ``v`` is the ranked list of 0's and 1's, represented by a NumPy array of
integers, ``X`` and ``L`` are the XL-mHG parameters, and the return values have
the following meanings:

- ``stat``: The XL-mHG test statistic
- ``cutoff``: The cutoff at which XL-mHG test statistic was attained
- ``pval``: The XL-mHG p-value

__ user_manual_

Documentation
-------------

Please refer to the `XL-mHG User Manual`__ (hosted on ReadTheDocs).

__ user_manual_

Citing XL-mHG
-------------

If you use the XL-mHG test in your research, please cite `Eden et al. (PLoS
Comput Biol, 2007)`__ and `Wagner (PLoS One, 2015)`__.

__ mhg_paper_
__ go_pca_paper_

Copyright and License
---------------------

Copyright (c) 2015-2017 Florian Wagner

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


.. _xlmhg_paper: https://doi.org/10.7287/peerj.preprints.1962v2

.. _zohar: http://bioinfo.cs.technion.ac.il/people/zohar

.. _mhg_paper: https://dx.doi.org/10.1371/journal.pcbi.0030039

.. _go_pca_paper: https://dx.doi.org/10.1371/journal.pone.0143196

.. _user_manual: https://xl-mhg.readthedocs.io

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
    :alt: Travis-CI build Status (master branch)
    :scale: 100%
    :target: https://travis-ci.org/flo-compbio/xlmhg.svg?branch=master

.. |travis-develop| image:: https://travis-ci.org/flo-compbio/xlmhg.svg?branch=develop
    :alt: Travis-CI build Status (develop branch)
    :scale: 100%
    :target: https://travis-ci.org/flo-compbio/xlmhg.svg?branch=develop

.. |appveyor-master| image:: https://ci.appveyor.com/api/projects/status/wpon7qkwpxx3fe6q/branch/master?svg=true
    :alt: Appveyor build Status (master branch)
    :scale: 100%
    :target: https://ci.appveyor.com/project/flo-compbio/xlmhg/branch/master

.. |appveyor-develop| image:: https://ci.appveyor.com/api/projects/status/wpon7qkwpxx3fe6q/branch/develop?svg=true
    :alt: Appveyor build Status (develop branch)
    :scale: 100%
    :target: https://ci.appveyor.com/project/flo-compbio/xlmhg/branch/develop

.. |codecov-master| image:: https://codecov.io/gh/flo-compbio/xlmhg/branch/master/graph/badge.svg
    :alt: Coverage (master branch)
    :target: https://codecov.io/gh/flo-compbio/xlmhg/branch/master

.. |codecov-develop| image:: https://codecov.io/gh/flo-compbio/xlmhg/branch/develop/graph/badge.svg
    :alt: Coverage (develop branch)
    :target: https://codecov.io/gh/flo-compbio/xlmhg/branch/develop

.. |docs-latest| image:: https://readthedocs.org/projects/xl-mhg/badge/?version=latest
    :alt: Documentation Status (master branch)
    :target: https://xl-mhg.readthedocs.io/en/latest

.. |docs-develop| image:: https://readthedocs.org/projects/xl-mhg/badge/?version=develop
    :alt: Documentation Status (develop branch)
    :target: https://xl-mhg.readthedocs.io/en/develop
