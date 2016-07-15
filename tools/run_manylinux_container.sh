#!/bin/bash
# requires docker, Python 3.5 and the `auditwheels` Python package
set -e -x

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pushd $DIR


### 64-bit

DOCKER_IMAGE=quay.io/pypa/manylinux1_x86_64
docker pull $DOCKER_IMAGE

# build Python 2.7 wheel
docker run --rm -v "`pwd`/..:/io" -e PYTHON_VERSION=2.7 $DOCKER_IMAGE \
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

# build Python 3.5 wheel
docker run --rm -v "`pwd`/..:/io" -e PYTHON_VERSION=3.5 $DOCKER_IMAGE linux32 \
    /io/tools/build_manylinux_wheel.sh


### clean up
pushd ..
mv wheelhouse/*.whl dist/
rm -r wheelhouse
popd

popd