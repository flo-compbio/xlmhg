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

Version 2.0
~~~~~~~~~~~

2.0.2 (2016-04-18)
------------------

- Integration with Travis CI

2.0.1 (2016-04-15)
------------------

- Fixed README.

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

For details regarding the algorithms, see
`Wagner (PeerJ Preprints, 2016) <https://doi.org/10.7287/peerj.preprints.1962v2>`_.
