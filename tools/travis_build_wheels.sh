#!/bin/bash

# Copyright (c) 2016-2019 Florian Wagner
#
# This file is part of XL-mHG.

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