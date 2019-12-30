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

Copyright (c) 2015-2019 Florian Wagner

::

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

    * Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


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
