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
  tools.snapshot(filename, x, y, z, radii, colour)
  #tools.snapshot(filename, x, y, z, x_jump, y_jump, z_jump, vx, vy, vz, vx,vy,vz,radii)
  tools.writePVD("particle.pvd")

def readParticle(filename, start, end):
  count = 0
  linecount = 0
  x = []
  y = []
  z = []
  vx = []
  vy = []
  vz = []
  partCount = 0
  colour = []
  radii = []
  timestep = 0.0001
  cutXMin = 120

  fout = open(filename[:-4]+"_solidvol.dat","w")
  fout2 = open(filename[:-4]+"_cordNo.dat","w")
  fout.write("Time Solid volume\n")
  with open(filename) as fin:
    for line in fin:
      count += 1
      remainder = linecount%int(skip)
      if(line.split()[0] == "TIME"):
        if(linecount > int(start)):
          if(remainder == 0):
            writeVtu("par"+str(linecount)+".vtu", x, y, z,radii, colour)
            print("Time No of particles ",str(linecount*timestep),partCount)
            fout.write(str(linecount*timestep)+" "+str(partCount)+"\n")

          partCount = 0
          # print(linecount)
          del x[:]
          del y[:]
          del z[:]
          del colour[:]
          del radii[:]

        linecount += 1
        if(linecount > int(end)):
          break
      elif (linecount > int(start)):
        xx = float(line.split()[0])
        yy = float(line.split()[1])
        zz = float(line.split()[2])
        x.append(round(xx,3))
        y.append(round(yy,3))
        z.append(round(zz,3))
        vx = float(line.split()[3])
        vy = float(line.split()[4])
        vz = float(line.split()[5])
        cord = line.split()[7]
        colour.append(round(np.sqrt(vx*vx+vy*vy+vz*vz),3))
        radii.append(round(float(line.split()[6]),3))
        if(xx > 100 and xx < 110 and zz < 0):
          partCount += 1
        if(xx > cutXMin):
          fout2.write(cord+"\n")
        # print(line)
  fout2.close()
  fout.close()
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
x_jump = []
y_jump = []
z_jump = []

x_force = []
y_force = []
z_force = []

readParticle(infile, start, end)
