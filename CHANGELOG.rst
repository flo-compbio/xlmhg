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

Changelog
=========

2.4.0 (2016-08-15)
------------------
- Added `get_result_figure()` API function to visualize test results using the
  Plotly offline plotting library (see https://plot.ly/python/offline/).
- Significantly expanded the documentation (added "installation" and
  "examples" sections).

2.4.1 (2016-08-22)
~~~~~~~~~~~~~~~~~~
- Added pip version 8 to dependencies (required for installing wheels).
- Fixed error in User Manual that resulting in missing documentation for the
  `get_result_figure` function.

2.4.3 (2016-10-19)
~~~~~~~~~~~~~~~~~~
- Fixed minor issue

2.4.7 (2017-01-14)
~~~~~~~~~~~~~~~~~~
- Added bottom panel to visualization of test result showing occurrences of the
  "1's"

2.3.0 (2016-08-08)
------------------
- Added arguments `exact_pval` and `escore_pval_thresh` to
  `get_xlmhg_test_result()`. Also, the `pval_thresh` argument now has a
  different meaning.

2.3.1 (2016-08-09)
~~~~~~~~~~~~~~~~~~
- Improved docstrings and added a user manual (https://xl-mhg.readthedocs.io)

2.2.7 (2016-07-20)
------------------
- Added binary distributions for Windows (32/64-bit), Mac OS X (10.6+
  64-bit), and Linux (32/64-bit), for both Python 2.7 and Python 3.5. This
  means that for all of these platforms/environments, the installation of the
  `xlmhg` package (`pip install xlmhg`) no longer requires a C compiler to
  be present.

2.2.0 (2016-05-03)
------------------
- Changed internal structure used to represent lists, from vector of size N
  to vector containing only the indices of the 1's. This saves memory and
  avoids storing redundant information.
- Added the `get_xlmhg_test_result()` front-end function, which returns an
  `mHGResult` object.

2.1.x updates
-------------
- 2.1.1 (2016-05-01): Fixed readme

2.1.0 (2016-05-01)
------------------
- Added Cython implementation for calculating XL-mHG E-scores
- Added `mHGResult` class for representing test results
- Added tests
- Fixed a few minor issues

2.0.x updates
-------------
- 2.0.7 (2016-04-21): Fixed small problem in setup script
- 2.0.5 (2016-04-19): Fixed an uninstended change introduced in 2.0.4 whereby
  a cythonized version instead of the mhg_cython.pyx file was included in the
  package
- 2.0.4 (2016-04-19): Added tests/ and CHANGELOG.rst to Manifest.in file
- 2.0.3 (2016-04-18): Including Travis CI build status in Readme
- 2.0.2 (2016-04-18): Integration with Travis CI
- 2.0.1 (2016-04-15): Readme fixes

2.0.0 (2016-04-15)
------------------
Major release with several new features:

- New API (`xlmhg.xlmhg_test()`; see `test.py`).
- Implementation of ``PVAL2`` algorithm for calculating XL-mHG p-values.
  This algorithm offers better performance and numerical stability and is
  now used by default.
- Implementation of ``PVAL-BOUND`` algorithm for calculating O(N)-bound.
- Implementation of ``PVAL-THRESH`` algorithm for deciding whether the
  XL-mHG p-value meets a given signifance level.
- Unit tests to ensure the correctness of all algorithms (using `pytest`).

For details regarding the algorithms, see `Wagner (PeerJ Preprints, 2016)
<https://doi.org/10.7287/peerj.preprints.1962v2>`_.
