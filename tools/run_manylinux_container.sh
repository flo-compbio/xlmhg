#!/bin/bash

# Copyright (c) 2016-2019 Florian Wagner
#
# This file is part of XL-mHG.

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

# build Python 3.5 wheel
docker run --rm -v "`pwd`/..:/io" -e PYTHON_VERSION=3.5 $DOCKER_IMAGE \
    /io/tools/build_manylinux_wheel.sh

# build Python 3.6 wheel
docker run --rm -v "`pwd`/..:/io" -e PYTHON_VERSION=3.6 $DOCKER_IMAGE \
    /io/tools/build_manylinux_wheel.sh

# build Python 3.7 wheel
docker run --rm -v "`pwd`/..:/io" -e PYTHON_VERSION=3.7 $DOCKER_IMAGE \
    /io/tools/build_manylinux_wheel.sh

# build Python 3.8 wheel
docker run --rm -v "`pwd`/..:/io" -e PYTHON_VERSION=3.8 $DOCKER_IMAGE \
    /io/tools/build_manylinux_wheel.sh

### 32-bit

DOCKER_IMAGE=quay.io/pypa/manylinux1_i686
docker pull $DOCKER_IMAGE

# build Python 3.5 wheel
docker run --rm -v "`pwd`/..:/io" -e PYTHON_VERSION=3.5 $DOCKER_IMAGE linux32 \
    /io/tools/build_manylinux_wheel.sh

# build Python 3.6 wheel
docker run --rm -v "`pwd`/..:/io" -e PYTHON_VERSION=3.6 $DOCKER_IMAGE linux32 \
    /io/tools/build_manylinux_wheel.sh

# build Python 3.7 wheel
docker run --rm -v "`pwd`/..:/io" -e PYTHON_VERSION=3.7 $DOCKER_IMAGE linux32 \
    /io/tools/build_manylinux_wheel.sh

# build Python 3.8 wheel
docker run --rm -v "`pwd`/..:/io" -e PYTHON_VERSION=3.8 $DOCKER_IMAGE linux32 \
    /io/tools/build_manylinux_wheel.sh

### clean up

pushd ..
mv wheelhouse/*.whl dist/
rm -r wheelhouse
popd

popd