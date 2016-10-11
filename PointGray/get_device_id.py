#!/usr/bin/env python

import subprocess
import sys

cmd = "readlink -f {0}".format( sys.argv[1] )
print( 'Executing %s' % cmd )
process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
# output of form /dev/videoX
out = process.communicate()[0]
# parse for ints
nums = [int(x) for x in out if x.isdigit()]
print( 'Device id is: %s' % nums[0] )

