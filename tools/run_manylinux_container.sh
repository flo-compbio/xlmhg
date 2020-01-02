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

### build 64-bit Python wheels
DOCKER_IMAGE=quay.io/pypa/manylinux1_x86_64
docker pull $DOCKER_IMAGE
docker run --rm -v "`pwd`/..:/io" -e PLAT="manylinux1_x86_64" $DOCKER_IMAGE \
    /io/tools/build_manylinux_wheels.sh

### build 32-bit Python wheels
DOCKER_IMAGE=quay.io/pypa/manylinux1_i686
docker pull $DOCKER_IMAGE
docker run --rm -v "`pwd`/..:/io" -e PLAT="manylinux1_i686" $DOCKER_IMAGE linux32 \
    /io/tools/build_manylinux_wheels.sh

### clean up
pushd ..
mv wheelhouse/*.whl dist/
rm -r wheelhouse
popd

popd