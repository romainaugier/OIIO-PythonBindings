#!/bin/bash

export __OLDPATH=$PATH
export __OLDPYTHONPATH=$PYTHONPATH

export PATH=$PWD/bin:$PATH
export PYTHONPATH=$PWD/bin:$PYTHONPATH
