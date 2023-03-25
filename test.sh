#!/bin/bash

source ./scripts/activate.sh

python tests/oiio_test.py

source ./scripts/deactivate.sh
