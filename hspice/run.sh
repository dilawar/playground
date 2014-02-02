#!/bin/bash
bnfc -m -haskell -d Jeera.cf
make 
./Jeera/Test < example.cir
