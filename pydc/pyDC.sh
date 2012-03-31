#!/bin/sh

export PYTHONPATH=`pwd`/pyDClib:`pwd`/pyDClib/he3:`pwd`/inter
python pydc.py $@
