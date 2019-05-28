#!/tools/python/2.6-x86_64/bin/python
from scipy.stats import f
# import pylab
import numpy as np
import os
import random
import math
import sys
import library.vtk_tools as vtk_t

from optparse import OptionParser, OptionValueError

def writeFile(infile, data):
  fout = open(infile,"w")
  for i in range(len(data)):
    fout.write(data[i]+"\n")
  fout.close()

# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')


# parse command line
p = OptionParser(usage="""usage: %prog [options] <infile>

Reads "particle.dat" file and extract partCollE, wallCollE, noOfPartColl, noOfWallCollE to part_data.dat
<infile> - particle.dat 

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")

(opts, args) = p.parse_args()

if len(args) != 1:
   p.print_help()
   sys.exit(1)
(infile) = args[0]

blockCount = 0
count = 0
data = {}

with open(infile) as fin:
  for line in fin:
        # break
      if(line.split()[0] == "TIME"):
        count = 0
        blockCount += 1
        print("BLOCK ",blockCount)
        # if(blockCount == int(block)):
        #   writeFile("wallColl.dat", noOfWallColl)
        #   writeFile("partColl.dat", noOfPartColl)
        #   writeFile("wallCollE.dat", wallCollE)
        #   writeFile("partCollE.dat", partCollE)
          
        #   break
        # del wallCollE[:]
        # del partCollE[:]
        # del noOfPartColl[:]
        # del noOfWallColl[:]
        
      else:
        count += 1
        vx = float(line.split()[3])
        vy = float(line.split()[4])
        vz = float(line.split()[5])
        velMag = np.sqrt(vx*vx+vy*vy+vz*vz)
        data[line.split()[11]] = [line.split()[7],line.split()[8],line.split()[9],line.split()[10],velMag,]
        
        # wallCollE.append(line.split()[7])
        # partCollE.append(line.split()[8])
        # noOfWallColl.append(line.split()[9])
        # noOfPartColl.append(line.split()[10])

print("SIZE ",len(data))
fout = open("part_data.dat","w")
for key,value in data.items():
  line = value[0]+" "+value[1]+" "+value[2]+" "+value[3]+" "+str(value[4])
  fout.write(str(key)+" "+line+"\n")
fout.close()

print("DONE")



