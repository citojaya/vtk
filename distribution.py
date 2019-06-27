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
  mean = np.mean(array)
  sigma = np.std(array,ddof=1)
  print("Sample Standard Deviation ",np.std(array,ddof=1))
  print("Mean ",np.mean(array))

  size = 40
  maxVal = max(array)
  minVal = min(array)
  binSize = (maxVal-minVal)/size
  total = sum(array)

  print("Bin Size ",binSize)
  print("Min and Max ",minVal,maxVal)
  print("Total ",total)

  binArray = np.array([])
  # for i in range(1,size+1):
  for i in range(size):
    binArray = np.append(binArray, [minVal+binSize*i],axis=0)

  # hist,bins = np.histogram(array,binArray)
  # plt.title("Total "+str(round(total,2))+" mean="+str(round(mean,3))+" sigma="+str(round(sigma,3)))
  plt.title(title+': $\mu='+str(round(mean,2))+'$, $\sigma='+str(round(sigma,2))+'$')
  # plt.title(title+"\n mean="+str(round(mean,3))+" sigma="+str(round(sigma,3)))
  plt.ylabel("Frequnecy")
  plt.xlabel(xLable)
  plt.hist(array,binArray)
  plt.show()

# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')


# parse command line
p = OptionParser(usage="""usage: %prog [options] <infile> <outfile> <col>

Reads input file and extract data in column "col" and plot frequency distribution
<infile> - input file
<outfile> - output file for the distribution 
<col> - which column of input file to be considered

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")

(opts, args) = p.parse_args()

if len(args) != 3:
   p.print_help()
   sys.exit(1)
(infile,outfile,col) = args

blockCount = 0
count = 0
data = []

dataArray = np.array([])

with open(infile) as fin:
  for line in fin:
    count += 1
    dataArray = np.append(dataArray,[float(line.split()[int(col)])],axis=0)
    # if(count == 20000):
    #   break
    

# dataArray = np.asarray(data)
dataArray = 1e-3*dataArray
print("SIZE ",len(dataArray))


# for i in range(len(data)):
#   dataArray = np.append(dataArray,[float(data[i])],axis=0)

# plotHistogram(dataArray, "Cell Drag force Fx (*1e6 N)","Drag force")
# plotHistogram(dataArray, "Porosity ","Porosity")
# plotHistogram(dataArray, "Cell gravity force (*1e6 N)","Cell gravity force")
# plotHistogram(dataArray, "Particle gravity force Fy (*1e6 N)","Cell gravity force")
# plotHistogram(dataArray, "Pressure Grad Fx (*1e6 N)", "Pressure Grad")
plotHistogram(dataArray, "Force (1e3 N/m3)", "Triangular Mesh")

print("DONE")



