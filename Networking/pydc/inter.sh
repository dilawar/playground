#!/bin/sh

cd inter

export PYTHONPATH=`pwd`/../pyDClib:`pwd`/../pyDClib/he3
export PYTHONSTARTUP=InterUtils.py
python

