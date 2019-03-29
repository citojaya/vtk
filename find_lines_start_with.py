#!/tools/python/2.6-x86_64/bin/python

import numpy as np
import os
import sys
from optparse import OptionParser, OptionValueError

# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')



# parse command line
p = OptionParser(usage="""usage: %prog [options] <inputfile><search><col>
Read <inputfile> and find line containing <search> and those lines will be writtne to "lines.dat"

<search> - serach for this string
<col>    - search string column

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 3:
   p.print_help()
   sys.exit(1)
(in_file, search, col) = args

out_data = []

f = open(in_file, "r")
for line in f:
  if not line.split():
    continue

  tuple = line.split()
  if tuple[int(col)-1] == search:
    out_data.append(line)

f.close()

f = open("lines.dat", 'w')
f.writelines(out_data)
f.close()

print "DONE"

