#!/tools/python/2.6-x86_64/bin/python
import numpy as np
import os
import random
import math
import sys
import library.vtk_tools as vtk_t

from optparse import OptionParser, OptionValueError



# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')


# parse command line
p = OptionParser(usage="""usage: %prog [options] 

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 1:
   p.print_help()
   sys.exit(1)
(infile) = args[0]

fout = open("_initial.inj","w")
with open(infile) as inf:
  for line in inf:
    tuple = line.split()
    # print(line)
    if(float(tuple[2]) < -2.5e-3):
      fout.write(line)

fout.close()


