#!/bin/bash

set -e -x

if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
  # linux
  # build wheels in manylinux1 docker container
  mkdir dist wheelhouse
  ls -alth
  ./tools/run_manylinux_container.sh
  codecov
else
  # mac
  python setup.py bdist_wheel
fi