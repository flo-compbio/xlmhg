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

# Builds manylinux1 wheels for the XL-mHG Python package using the
# manylinux1 docker image. This script requires docker to be installed.
# This script is called from travis_build_wheels.sh (whenever we're running on
# linux).

set -e -x

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pushd $DIR

### 64-bit

DOCKER_IMAGE=quay.io/pypa/manylinux1_x86_64
docker pull $DOCKER_IMAGE

# build Python 2.7 wheel
docker run --rm -v "`pwd`/..:/io" -e PYTHON_VERSION=2.7 $DOCKER_IMAGE \
    /io/tools/build_manylinux_wheel.sh

# build Python 3.4 wheel
docker run --rm -v "`pwd`/..:/io" -e PYTHON_VERSION=3.4 $DOCKER_IMAGE \
    /io/tools/build_manylinux_wheel.sh

# build Python 3.5 wheel
docker run --rm -v "`pwd`/..:/io" -e PYTHON_VERSION=3.5 $DOCKER_IMAGE \
    /io/tools/build_manylinux_wheel.sh


### 32-bit

DOCKER_IMAGE=quay.io/pypa/manylinux1_i686
docker pull $DOCKER_IMAGE

# build Python 2.7 wheel
docker run --rm -v "`pwd`/..:/io" -e PYTHON_VERSION=2.7 $DOCKER_IMAGE linux32 \
    /io/tools/build_manylinux_wheel.sh

# build Python 3.4 wheel
docker run --rm -v "`pwd`/..:/io" -e PYTHON_VERSION=3.4 $DOCKER_IMAGE linux32 \
    /io/tools/build_manylinux_wheel.sh

# build Python 3.5 wheel
docker run --rm -v "`pwd`/..:/io" -e PYTHON_VERSION=3.5 $DOCKER_IMAGE linux32 \
    /io/tools/build_manylinux_wheel.sh


### clean up
pushd ..
mv wheelhouse/*.whl dist/
rm -r wheelhouse
popd

popd