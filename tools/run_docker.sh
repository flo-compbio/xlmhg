#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pushd $DIR

DOCKER_IMAGE=quay.io/pypa/manylinux1_x86_64
docker pull $DOCKER_IMAGE
docker run --rm -v "`pwd`/..:/io" -e TRAVIS_PYTHON_VERSION=2.7 $DOCKER_IMAGE \
    /io/tools/build_manylinux_wheel.sh

popd