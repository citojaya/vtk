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
p = OptionParser(usage="""usage: %prog [options] <filename> <startframe> <endframe>

Generate particle.pvd upto <endframe>

<filename> - filename including path
<pvdfile> - pvd filename
<endframe> - end frame
<skip> - particle frame interval

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 4:
   p.print_help()
   sys.exit(1)
(filename, pvdfile, end, step) = args

skip = 0
f = open(pvdfile, "w")
f.write('<?xml version="1.0" ?>\n')
f.write('<VTKFile byte_order="LittleEndian" type="Collection" version="0.1">\n')
f.write('<Collection>\n')
for i in range(int(end)/int(step)):
  skip = skip+int(step)
  f.write('<DataSet file="'+filename+str(skip)+'.vtu" group="" part="0" timestep="'+str(i)+'"/>\n')

f.write('<Collection>\n')
f.write('</VTKFile>\n')

f.close()


