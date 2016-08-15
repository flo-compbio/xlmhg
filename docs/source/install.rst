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

Installation
============

Installing the xlmhg package should be straightforward on Linux,
Windows, and Mac OS X. It only requires `Python 2.7.x or 3.5.x`__ to be
installed. If you have a different version of Python, you have to `install
the package from source`__.

__ python_
__ source_

.. note::

    To see which version of Python you're running, you can always run
    ``python -V`` in a terminal / command prompt window. Alternatively, you
    can run the following in Python:

    .. code-block:: python

        import sys
        print(sys.version)

The XL-mHG software is hosted on `PyPI`__, the central repository for
Python packages. The recommended installation procedure on Linux, Windows, and
Mac OS X is using `pip`__, the main tool for installing Python packages.

__ pypi_
__ pip_

Installing the latest version
-----------------------------

To install the latest version of the `xlmhg`__ Python package, run::

    pip install xlmhg

__ xlmhg_


Installing a specific version
-----------------------------

To install a specific version of the `xlmhg`__ Python package, e.g., "2.3.1",
run::

    pip install xlmhg==2.3.1


__ xlmhg_

Specifying a version range
--------------------------

XL-mHG follows `semantic versioning`__, so changes in the major release number
(e.g., 1.x.x vs. 2.x.x) indicate a backwards-incompatible API change. To
install the latest version of a specific major release number (e.g., "2.x.x"),
run::

    pip install "xlmhg>=2,<3"

__ semvar_

.. _source:

Installation from source
------------------------

This installation method is only required for Python versions other than 2.7
or 3.5. The installation command is the same (``pip install xlmhg``), but
the installation involves the compilation of C source code using a C compiler.
The procedure for installing an appropriate compiler is different for different
operating systems.

Ubuntu Linux
~~~~~~~~~~~~

Do the following to install the gcc compiler (requires root privileges):

.. code-block:: bash

    $ apt-get install build-essential

Windows
~~~~~~~

For Python 2.6-3.2, use the Microsoft Visual Studio 2008 compiler
(`32-bit`__ / `64-bit`__). For Python 3.3 and 3.4, use the Visual Studio
2010 compiler (`32-bit`__ / `64-bit`__).

__ vs2008-32_
__ vs2008-64_
__ vs2010-32_
__ vs2010-64_

.. _python: https://www.python.org/downloads/

.. _pypi: https://pypi.python.org/pypi

.. _pip: https://pip.pypa.io/en/stable/

.. _xlmhg: https://pypi.python.org/pypi/xlmhg

.. _semvar: http://semver.org/

.. _vs2008-32: https://www.microsoft.com/en-us/download/details.aspx?id=29

.. _vs2008-64: https://www.microsoft.com/en-us/download/details.aspx?id=15336

.. _vs2010-32: https://www.microsoft.com/en-us/download/details.aspx?id=5555

.. _vs2010-64: https://www.microsoft.com/en-us/download/details.aspx?id=14632