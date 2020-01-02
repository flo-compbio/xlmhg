#!/bin/bash

# Copyright (c) 2020 Florian Wagner
#
# This file is part of XL-mHG.

# Builds manylinux1 wheels for the XL-mHG Python package using the
# manylinux1 docker image. This script is run inside the docker container.

set -e -x

cd ~
echo "The current working directory is: `pwd`"

PYVERSIONS=(cp35-cp35m cp36-cp36m cp37-cp37m cp38-cp38)

# Compile wheels
for PYVER in ${PYVERSIONS[*]}; do
    PYBIN="/opt/python/${PYVER}/bin"
    "${PYBIN}/pip" install -r /io/dev-requirements.txt
    "${PYBIN}/pip" wheel /io -w wheelhouse
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/xlmhg-*.whl; do
    auditwheel repair "$whl" --plat $PLAT -w /io/wheelhouse
done

# Install packages and test
for PYVER in ${PYVERSIONS[*]}; do
    PYBIN="/opt/python/${PYVER}/bin"
    "${PYBIN}/pip" install xlmhg --no-index -f /io/wheelhouse
    (cd "$HOME"; "${PYBIN}/pytest" /io )
done