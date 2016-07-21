#!/bin/bash

# Copyright (c) 2016 Florian Wagner
#
# This file is part of XL-mHG.
#
# XL-mHG is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License, Version 3,
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# This script is called from ".travis.yml". Depending on whether we are
# building on linux or on OS X, we perform different actions to build the
# wheels for that platform.

set -e -x

if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
  # linux
  # upload coverage report to codecov.io
  codecov
  # build wheels in manylinux1 docker container
  mkdir dist wheelhouse
  ls -alth
  ./tools/run_manylinux_container.sh
else
  # mac
  python setup.py bdist_wheel
fi