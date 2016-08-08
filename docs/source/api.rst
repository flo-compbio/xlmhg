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


API Reference
=============

The `xlmhg <https://pypi.python.org/pypi/xlmhg>`_ package offers two
alternative Python APIs (functions) to perform an XL-mHG test:

- The :ref:`simple API <simple_api>` (:func:`xlmhg.xlmhg_test`) accepts a
  ranked list in the form of a vector, and (optionally) the ``X`` and ``L``
  parameters, and returns a 3-tuple containing the test statistic, cutoff,
  and p-value.

- The :ref:`advanced API <advanced_api>` (:func:`xlmhg.get_xlmhg_test_result`)
  accepts a more compact representation of a ranked list (consisting of its
  length ``N`` and a vector specifying the ``indices`` of the 1's in the ranked
  list), as well as several additional arguments that can improve the
  performance of the test. Instead of a simple tuple, this API returns the test
  result as an `mHGResult` object, which includes additional information such
  as the parameters used to perform the test, and methods to calculate
  additional quantities like E-Scores.

.. _simple_api:

Simple API
----------

.. autofunction:: xlmhg.xlmhg_test


.. _advanced_api:

Advanced API
------------

.. autofunction:: xlmhg.get_xlmhg_test_result


.. "Indices and tables
    ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

.. autoclass:: xlmhg.mHGResult
    :members: