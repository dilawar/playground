#!/bin/bash - 
#===============================================================================
#
#          FILE: test_using_coriander.sh
# 
#         USAGE: ./test_using_coriander.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Dilawar Singh (), dilawars@ncbs.res.in
#  ORGANIZATION: NCBS Bangalore
#       CREATED: Tuesday 11 October 2016 01:33:30  IST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
set -x
set -e
export DC1394_DEBUG=1
coriander
