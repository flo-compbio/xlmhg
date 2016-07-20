#!/bin/bash

set -e -x

mkdir dist wheelhouse
ls -alth
./tools/run_manylinux_container.sh
codecov