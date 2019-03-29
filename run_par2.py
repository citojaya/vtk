#!/tools/python/2.6-x86_64/bin/python
import numpy as np
import os
import random
import math
import sys
import library.vtk_tools as vtk_t

from optparse import OptionParser, OptionValueError

def writeVtu(filename, x, y, z, radii, colour): 
  print(filename)
  #vtu_file = "par"+str(no_of_files)+".vtu"
  if opts.verbose:print "Writing ",filename
  tools.snapshot(filename, x, y, z, x_jump, y_jump, z_jump, x_force, y_force, z_force, radii, colour)
  #tools.snapshot(filename, x, y, z, x_jump, y_jump, z_jump, vx, vy, vz, vx,vy,vz,radii)
  tools.writePVD("particle.pvd")

def readParticle(filename, nfrm):
  count = 0

  #prevcount = 0
  with open(filename) as fin:
  #fin = open("particle.dat", "r") 
    for line in fin: 
    #line = fin.readline()
      #print(line)
      if(line.split()[0] == "TIME"):
        if(count > 0):
          writeVtu("par"+str(count)+".vtu", x, y, z,radii, colour)
        x = []
        y = []
        z = []
        vx = []
        vy = []
        vz = []
        colour = []
        radii = []
        count += 1
      
      #if(coun > prevcount):
      #  prevcount = count
      else:
        x.append(round(float(line.split()[0]),3))
        y.append(round(float(line.split()[1]),3))
        z.append(round(float(line.split()[2]),3))
        #vx.append(round(float(line.split()[3]),3))
        #vy.append(round(float(line.split()[4]),3))
        #vz.append(round(float(line.split()[5]),3))
        #radii.append(0.5*(float(tuple[6])))
        vx = float(line.split()[3])
        vy = float(line.split()[4])
        vz = float(line.split()[5])
        colour.append(round(np.sqrt(vx*vx+vy*vy+vz*vz),3))
        #radii.append(0.13)
        radii.append(round(float(line.split()[6]),3))
        #print(line)    
      if(count > int(nfrm)):
        break

# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')


# parse command line
p = OptionParser(usage="""usage: %prog [options] <infile> <endframe>

Reads "particle.dat" file and constructs "particle.pvd" which contains particle information 
for PARAVIEW visualization 


""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 2:
   p.print_help()
   sys.exit(1)
(infile, nframes) = args

tools = vtk_t.VTK_XML_Serial_Unstructured()
x_jump = []
y_jump = []
z_jump = []

x_force = []
y_force = []
z_force = []

readParticle(infile, nframes)
