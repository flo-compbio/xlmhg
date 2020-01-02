#!/bin/bash

set -e -x

cd ~
echo "The current working directory is: `pwd`"

PYVERSIONS=(cp35-cp35m cp36-cp36m cp37-cp37m cp38-cp38)
PLAT=manylinux1_x86_64

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
#echo "TESTING PHASE!"
#for PYVER in ${PYVERSIONS[*]}; do
#    PYBIN="/opt/python/${PYVER}/bin"
#    "${PYBIN}/pip" install xlmhg --no-index -f /io/wheelhouse
#    (cd "$HOME"; "${PYBIN}/pytest" .)
#done