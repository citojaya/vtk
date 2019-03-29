#!/tools/python/2.6-x86_64/bin/python

import os
import sys

import re
from optparse import OptionParser, OptionValueError

import numpy as np

import glob
import vtk
from vtk.util import numpy_support

# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')


# parse command line
p = OptionParser(usage="""
<program> <prefix><no_of_files><out_file>

Read list of files containing particle position and create a combined file
Ex: combine_files.py out_par 100 combined.dat
""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")
p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, .vtu output")
(opts, args) = p.parse_args()


# Get the arguments
if len(args) != 3:
  print "Program must be called with 2 arguments"
  p.print_help()
  sys.exit(1)
(prefix,no_of_files,out_file) = args



#list_of_files = glob.glob(casename+'*.history')
out_data = []

s = ''
for i in range(int(no_of_files)):
  f = open(prefix+str(i+1)+".dat", 'r')
  data = f.readline()
  out_data.append(data)
  f.close()

f = open(out_file,"w")
f.writelines(out_data)
f.close()

print "DONE"


