#!/bin/bash

which python
if [ $? -ne 0 ]
then
    echo "Python can't be found, please install it and make it available in the PATH before continuing"
    exit 1
else
    echo "Found Python"
fi

which cmake
if [ $? -ne 0 ]
then 
    echo "CMake can't be found, please install it and make it available in the PATH before continuing"
    exit 1
else
    echo "Found CMake"
fi

which conan 
if [ $? -ne 0 ]
then
    echo "Conan not found, making virtual environment to install it"
    python -m venv env
    source env/bin/activate
    pip install conan==1.59
else
    conan --version | grep "1.59"
    if [ $? -ne 0 ]
    then
        echo "Conan version supportedd is 1.59.0, please install it or make a new virtual environment"
        exit 1
    fi

    echo "Conan 1.59.0 found"
fi

cd openimageio2.4
conan create . openimageio/2.4@pythonbindings/1.0 -o with_ffmpeg=False -o *:shared=True --build missing

cd ..
conan install .

PYDIR=$(find . -type d -not -path "./bin/*" | grep "site-packages/OpenImageIO")
PYDIR="${PWD}${PYDIR:1}"

cp -a "${PYDIR}/." "./bin"

PYDIR="${PYDIR//$"site-packages/OpenImageIO"/}"

rm -rf $PYDIR

cd bin

PYDIR=$(find . -type d | grep "site-packages/OpenImageIO")
PYDIR="${PWD}${PYDIR:1}"

mv "${PYDIR}"/* "./"

PYDIR="${PYDIR//$"site-packages/OpenImageIO"/}"

rm -rf $PYDIR
