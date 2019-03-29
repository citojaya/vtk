#!/tools/python/2.6-x86_64/bin/python
import numpy as np
import os
import random
import math
import sys
import library.vtk_tools as vtk_t
import glob
from optparse import OptionParser, OptionValueError



# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')


# parse command line
p = OptionParser(usage="""usage: %prog [options]<prefix>

Reads "*_1.txt" (Esys particles) files and constructs "particle.pvd" which contains particle information for PARAVIEW visualization 

Ex:
If the output file is in "mill_t=400000_1.txt" format
prefix should be "mill"


""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 1:
   p.print_help()
   sys.exit(1)
(prefix) = args[0]

tools = vtk_t.VTK_XML_Serial_Unstructured()
no_of_files = 0

list_of_files_dict = {}
list_of_files = glob.glob(prefix+"_t="+"*"+"_1.txt")
for filename in list_of_files:
  file_no = filename[len(prefix)+3:-6]
  list_of_files_dict[int(file_no)]=filename

keylist = list_of_files_dict.keys()
keylist.sort()


for key in keylist:
  no_of_files += 1
  filename = list_of_files_dict[key]

  if opts.verbose:print "Writing file",filename
  f = open(filename, 'r')
  data = f.readlines()
  f.close()

  x = []
  y = []
  z = []

  x_jump = []
  y_jump = []
  z_jump = []

  x_force = []
  y_force = []
  z_force = []

  radii = []
  color = []

  no_of_particles = int(data[0])
  for i in range(1,no_of_particles):
    line = data[i].strip()
    tuple = line.split()
  
    x.append(float(tuple[0]))
    y.append(float(tuple[1]))
    z.append(float(tuple[2]))
    radii.append(float(tuple[3]))
    color.append(float(tuple[6]))
  vtu_file = "par"+str(no_of_files)+".vtu"
  tools.snapshot(vtu_file, x, y, z, x_jump, y_jump, z_jump, x_force, y_force, z_force, radii, color)
#val.snapshot("filename.vtu", x, y, z)
  tools.writePVD("particle.pvd")

