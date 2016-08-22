..
    Copyright (c) 2016 Florian Wagner

    This file is part of XL-mHG.

    XL-mHG is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License, Version 3,
    as published by the Free Software Foundation.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.

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
