#!/usr/bin/env bash
set -e
set -x
OUTDIR=/tmp/DILAWAR
if [ -d $OUTDIR ]; then rm -rf $OUTDIR; fi
kiwi-ng --type vmx system build  \
    --description kiwi-descriptions/suse/x86_64/suse-leap-15.1-JeOS  \
    --target-dir /tmp/DILAWAR
