#!/tools/python/2.6-x86_64/bin/python
from scipy.stats import f
from matplotlib import pyplot as plt
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

def logNormal():
  return 0

def plotHistogram(array, xLable, title):
  print("Sample Standard Deviation ",np.std(array,ddof=1))
  print("Mean ",np.mean(array))

  size = 40
  maxVal = max(array)
  minVal = min(array)
  binSize = (maxVal-minVal)/size

  print("Bin Size ",binSize)
  print("Min and Max ",minVal,maxVal)

  binArray = np.array([])
  for i in range(1,size+1):
    binArray = np.append(binArray, [binSize*i],axis=0)

  # hist,bins = np.histogram(array,binArray)
  plt.title(title)
  plt.ylabel("Frequnecy")
  plt.xlabel(xLable)
  plt.hist(array,binArray)
  plt.show()

# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')


# parse command line
p = OptionParser(usage="""usage: %prog [options] <infile> <outfile> <frame>

Reads "particle.dat" file and extract   wallCollE, partCollE,  noOfWallColl, noOfPartColl, velocity to part_data.dat
<infile> - particle.dat
<outfile> - output file name
<frame> - particle snapshot

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")

(opts, args) = p.parse_args()

if len(args) != 3:
   p.print_help()
   sys.exit(1)
(infile,outfile,frame) = args

blockCount = 0
count = 0
data = {}

with open(infile) as fin:
  for line in fin:
      if(line.split()[0] == "TIME"):
        count = 0
        blockCount += 1
        print("BLOCK ",blockCount)
       
      else:
        count += 1
        vx = float(line.split()[3])
        vy = float(line.split()[4])
        vz = float(line.split()[5])
        velMag = np.sqrt(vx*vx+vy*vy+vz*vz)
        data[line.split()[11]] = [line.split()[7],line.split()[8],line.split()[9],line.split()[10],velMag,]
      
      if(int(frame)) == blockCount:
        break

val = 2
velArray = np.array([])
ppCollArray = np.array([])
pwCollArray = np.array([])
ppCollEArray = np.array([])
pwCollEArray = np.array([])

print("SIZE ",len(data))
fout = open(outfile+".dat","w")
for key,value in data.items():
  line = value[0]+" "+value[1]+" "+value[2]+" "+value[3]+" "+str(value[4])
  fout.write(str(key)+" "+line+"\n")
  velArray = np.append(velArray,[float(value[4])],axis=0)
  ppCollArray = np.append(ppCollArray,[float(value[3])],axis=0)
  pwCollArray = np.append(pwCollArray,[float(value[2])],axis=0)
  ppCollEArray = np.append(ppCollEArray,[float(value[1])*1e-3],axis=0)
  pwCollEArray = np.append(pwCollEArray,[float(value[0])*1e-3],axis=0)

fout.close()

print("written to "+outfile+".dat")

plotHistogram(ppCollArray, "","Particle-Particle Collision Frequnecy")
plotHistogram(pwCollArray, "","Particle-Wall Collision Frequnecy")
# plotHistogram(ppCollEArray, "Collision Energy (1e-9 J)", "Particle-Particle Collision Energy Distribution")
# plotHistogram(pwCollEArray)
plotHistogram(velArray, "Velocity (m/s)", "Velocity Distribution")

# plt.plot(velArray,binArray)

print("DONE")



