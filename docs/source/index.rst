.. XL-mHG documentation master file, created by
   sphinx-quickstart on Mon Aug  8 10:28:06 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

XL-mHG User Manual
==================

.. toctree::
  :maxdepth: 2

The `xlmhg <https://pypi.python.org/pypi/xlmhg>`_ package offers two
alternative Python APIs (functions) to perform an XL-mHG test:

- The :ref:`simple API <simple_api>` (:func:`xlmhg_test`) accepts a ranked
  list in the form of a vector, and (optionally) the ``X`` and ``L``
  parameters, and returns a 3-tuple containing the test statistic, cutoff,
  and p-value.

- The :ref:`advanced API <advanced_api>` accepts a more compact representation
  of a ranked list (consisting of its length ``N`` and a vector specifying
  the ``indices`` of the 1's in the ranked list), as well as several additional
  arguments that can improve the performance of the test. Instead of a
  simple tuple, this API returns the test result as an `mHGResult` object,
  which includes additional information such as the parameters used to perform
  the test, and methods to calculate additional quantities like E-Scores.


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