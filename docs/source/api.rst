..
    Copyright (c) 2016-2019 Florian Wagner

    This file is part of XL-mHG.

.. currentmodule:: xlmhg


API Reference
=============

The `xlmhg <https://pypi.python.org/pypi/xlmhg>`_ Python API includes two
alternative functions to **conduct an XL-mHG test**:

- The :ref:`simple test function <simple_test>`, :func:`xlmhg_test`,
  accepts a ranked list in the form of a vector, and (optionally) the ``X``
  and ``L`` parameters, and returns a 3-tuple containing the test statistic,
  cutoff, and p-value.

- The :ref:`advanced test function <advanced_test>`,
  :func:`get_xlmhg_test_result`, accepts a more compact representation
  of a list (consisting of its length ``N`` and a vector specifying the
  ``indices`` of the 1's in the ranked list), as well as several additional
  arguments that can improve the  performance of the test. Instead of a
  simple tuple, this API returns the test result as an :class:`mHGResult`
  object, which includes additional information such as the test parameters,
  and methods to calculate additional quantities like E-Scores.

Additionally, the API includes a function,
:func:`get_result_figure`, for **visualizing a test result** in a
`Plotly`__ figure. See :doc:`examples` for concrete examples of
how to use these functions.

__ plotly_

.. _simple_test:

Simple test function - :func:`xlmhg_test`
-----------------------------------------

.. autofunction:: xlmhg_test


.. _advanced_test:

Advanced test function - :func:`get_xlmhg_test_result`
------------------------------------------------------

.. autofunction:: xlmhg.get_xlmhg_test_result

Test result objects - :class:`mHGResult`
----------------------------------------

.. autoclass:: xlmhg.mHGResult
    :members:

Visualizing test results - :func:`get_result_figure`
----------------------------------------------------

.. autofunction:: xlmhg.get_result_figure

.. _plotly: https://plot.ly/


.. "Indices and tables
    ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
