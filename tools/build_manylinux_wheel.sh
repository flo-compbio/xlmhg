#!/bin/bash
set -e -x

# this should be run from within a manylinux docker container

cd ~
echo "The current working directory is: `pwd`"

# install conda
if [[ "${TRAVIS_PYTHON_VERSION}" == "2.7" ]]; then
    curl -o miniconda.sh https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
else
    curl -o miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
fi
bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
hash -r
conda config --set always_yes yes --set changeps1 yes
conda update -q conda
conda info -a

# set up python environment
conda create -q -n buildenv python=${TRAVIS_PYTHON_VERSION}
source activate buildenv

# upgrade pip
pip install --upgrade pip
pip install --upgrade --ignore-installed setuptools

# install requirements for building the package
pip install --upgrade wheel numpy cython auditwheel six

# get ready to build
cd /io
echo "The current working directory is: `pwd`"
python setup.py bdist_wheel
#auditwheel repair dist/*.whl
#rm dist/*.whl
#mv wheelhouse/*.whl dist/