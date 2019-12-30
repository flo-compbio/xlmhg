#!/bin/bash

# Copyright (c) 2016-2019 Florian Wagner
#
# This file is part of XL-mHG.

# Helper script to run the manylinux build command with sudo and PATH variable
# set correctly. This script is useful to manually build manylinux1 wheels for
# the XL-mHG Python package.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pushd $DIR
sudo "PATH=$PATH" ./run_manylinux_container.sh
popd