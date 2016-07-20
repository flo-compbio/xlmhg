#!/bin/bash

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