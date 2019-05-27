#!/tools/python/2.6-x86_64/bin/python
import numpy as np
import os
import random
import math
import sys
import library.vtk_tools as vtk_t

from optparse import OptionParser, OptionValueError

def writeVtu(filename, x, y, z, vx, vy, vz): 
  print(filename)
  if opts.verbose:print "Writing ",filename
  tools.snapshotVel(filename, x, y, z, vx, vy, vz)
  tools.writePVD("velocity.pvd")


def readVelocityField(filename, start, end):
  count = 0
  linecount = 0
  x = []
  y = []
  z = []
  vx = []
  vy = []
  vz = []
  timestep = 0.0001
  
  with open(filename) as fin:
    for line in fin:
      count += 1
      remainder = linecount%int(skip)
      if(line.split()[0] == "TIME"):
        if(linecount > int(start)):
          if(remainder == 0):
            writeVtu("vel"+str(linecount)+".vtu", x,y,z,vx,vy,vz)
            # print("Time No of particles ",str(linecount*timestep),partCount)
            # fout.write(str(linecount*timestep)+" "+str(partCount)+"\n")

          partCount = 0
          # print(linecount)
          del x[:]
          del y[:]
          del z[:]
          del vx[:]
          del vy[:]
          del vz[:]

        linecount += 1
        if(linecount > int(end)):
          break
      elif (linecount > int(start)):
        xx = float(line.split()[0])
        yy = float(line.split()[1])
        zz = float(line.split()[2])
        vxx = float(line.split()[3])
        vyy = float(line.split()[4])
        vzz = float(line.split()[5])

        x.append(round(xx,3))
        y.append(round(yy,3))
        z.append(round(zz,3))
        vx.append(round(vxx,3))
        vy.append(round(vyy,3))
        vz.append(round(vzz,3))

 


# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')


# parse command line
p = OptionParser(usage="""usage: %prog [options] <infile> <startframe> <endframe> <skip>

Reads "particle.dat" file and constructs "particle.pvd" which contains particle information 
for PARAVIEW visualization 

<start> - start frame
<endframe> - end frame
<skip> - skip this many frames

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 4:
   p.print_help()
   sys.exit(1)
(infile, start, end, skip) = args

tools = vtk_t.VTK_XML_Serial_Unstructured()
readVelocityField(infile, start, end)
