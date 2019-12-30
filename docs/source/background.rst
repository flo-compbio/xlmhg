..
    Copyright (c) 2016-2019 Florian Wagner

    This file is part of XL-mHG.

Statistical Background
======================

The XL-mHG test is a powerful semiparametric test to assess *enrichment* in
ranked lists. It is based on the nonparametric **mHG test**, developed by
`Dr. Zohar Yakhini`__ and colleagues (`Eden et al., 2007`__), who also proposed
a dynamic programming algorithm that enables the efficient calculation of
exact p-values for this test.

__ zohar_
__ mhg_paper_

The input to the test is a ranked list of items, some of which are known
to have some "interesting property". The test asks whether there exists an
unusual accumulation of a subset of those "interesting items" at the "top of
the list", without requiring the user to specify what part of the list should
be considered "the top". Computationally, the ranked list can be represented
as a column vector containing only 0's and 1's, with 1's representing the
interesting items. For example, the following list of 20 items exhibits an
accumulation of 1's "at the top" that is considered statistically significant
(p < 0.05) by the mHG test:

v = (1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)\ :sup:`T`

To better understand how enrichment is defined for the purposes of the mHG
test, it is helpful to take a close
look at the definition of its test statistic: For a given ranked list of length
``N``, it is defined as the *minimum hypergeometric p-value* over all N
possible cutoffs. This means that users do not have to specify a fixed
cutoff that defines "the top of the list". This nonparametric approach makes
the mHG test very flexible, meaning that it can detect enrichment when there
are only a few "interesting" items that are extremely concentrated at the very
top of the list (representing one extreme), as well as when there is a
slight overabundance of interesting items within, say, the entire top half
of the list.

However, for some applications, the mHG test is a little "too flexible",
meaning that it would be beneficial to be able to somewhat restrict the type of
enrichment that is being detected by the test. To this end, the **XL-mHG test**
extends the mHG test, by introducing two parameters (``X`` and ``L``) that
essentially allow certain cutoffs to be ignored in the calculation of the
test statistic. The `xlmhg`__ package implements a dynamic programming
algorithm to efficiently calculate XL-mHG p-values. This algorithm is based on
the algorithm proposed by `Eden et al.`__, but has been modified to calculate
exact p-values for the new test statistic, (`Wagner, 2015`__), and improved
to provide better numerical accuracy and performance (`Wagner, 2016`__).

__ xlmhg_
__ mhg_paper_
__ mhg_TR_
__ xlmhg_paper_

In biology, specifically in *GO enrichment analysis*, there are many situations
in which the "best" cutoff is not known *a priori*. In those cases, the
mHG and XL-mHG tests are excellent choices for detecting enrichment, and
have been successfully applied for detecting GO enrichment in both supervised
and unsupervised settings (`Eden, Navon, et al., 2007`__; `Wagner, 2015`__).

__ gorilla_paper_
__ go_pca_paper_


What do the ``X`` and ``L`` parameters mean?
--------------------------------------------

- ``X`` refers to the minimum number of "1's" that have to be seen before
  anything can be called "enrichment".
- ``L`` is the lowest cutoff (i.e., the largest ``n``) that is being tested
  for enrichment.

A more direct way to understand ``X`` and ``L`` is through the definition of
the XL-mHG test statistic. It is defined as the minimum hypergeometric p-value
over all cutoffs at which at least ``X`` "1's" have already been seen, and
excluding any cutoffs larger than ``L``. For ``X=1`` and ``L=N``, the XL-mHG
test reduces to the mHG test.

Further reading
---------------

For detailed discussions of the XL-mHG test and the algorithms
implemented in the `xlmhg`__ package to efficiently calculate XL-mHG test
statistics and p-values, please see the
`Technical Report on arXiv (Wagner, 2015)`__,
as well as the `XL-mHG PeerJ Preprint article (Wagner, 2016)`__.

__ xlmhg_
__ mhg_TR_
__ xlmhg_paper_

.. _xlmhg: https://github.com/flo-compbio/xlmhg

.. _mhg_TR: https://arxiv.org/abs/1507.07905

.. _zohar: http://bioinfo.cs.technion.ac.il/people/zohar

.. _mhg_paper: https://dx.doi.org/10.1371/journal.pcbi.0030039

.. _xlmhg_paper: https://doi.org/10.7287/peerj.preprints.1962v2

.. _gorilla_paper: https://dx.doi.org/10.1186/1471-2105-10-48

.. _go_pca_paper: https://dx.doi.org/10.1371/journal.pone.0143196
