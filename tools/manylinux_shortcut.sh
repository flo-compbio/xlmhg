#!/bin/bash
# helper script to run the manylinux build command with sudo and PATH variable set

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pushd $DIR
sudo "PATH=$PATH" ./run_manylinux_container.sh
popd