#!/tools/python/2.6-x86_64/bin/python
from scipy.stats import f
from matplotlib import pyplot as plt
import matplotlib.mlab as mlab
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

def plotProbDensity(array):
    mu = np.mean(array)
    sigma = np.std(array,ddof=1)
    x = mu + sigma*array
    num_bins = 50
    fig, ax = plt.subplots()

    # the histogram of the data
    n, bins, patches = ax.hist(x, num_bins, normed=1)

    # add a 'best fit' line
    y = mlab.normpdf(bins, mu, sigma)
    ax.plot(bins, y, '--')
    ax.set_xlabel('Porosity')
    ax.set_ylabel('Probability density')
    ax.set_title(r'Histogram of instant porosity: $\mu='+str(round(mu,3))+'$, $\sigma='+str(round(sigma,3)) +'$')

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.show()


def plotHistogram(array):
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

  plt.ylabel("Frequnecy")
  plt.xlabel("Porosity")
  plt.hist(array,binArray)
  plt.show()

# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')


# parse command line
p = OptionParser(usage="""usage: %prog [options] <infile> <outfile>

Reads "logfile5.log" file and extract porosity to por_data.dat
<infile> - logfile5.log
<outfile> - output file name

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")

(opts, args) = p.parse_args()

if len(args) != 2:
   p.print_help()
   sys.exit(1)
(infile,outfile) = args

blockCount = 0
count = 0
data = np.array([])

with open(infile) as fin:
  for line in fin:
      if(float(line.split()[1]) < 0.9):
        count += 1
        if(count < 4869):
            por = float(line.split()[1])
            data = np.append(data,por)

print("SIZE ",len(data))
# fout = open(outfile+".dat","w")
# for key,value in data.items():
#   line = value[0]+" "+value[1]+" "+value[2]+" "+value[3]+" "+str(value[4])
#   fout.write(str(key)+" "+line+"\n")
#   velArray = np.append(velArray,[float(value[4])],axis=0)
#   ppCollArray = np.append(ppCollArray,[float(value[3])],axis=0)
#   pwCollArray = np.append(pwCollArray,[float(value[2])],axis=0)
#   ppCollEArray = np.append(ppCollEArray,[float(value[1])],axis=0)
#   pwCollEArray = np.append(pwCollEArray,[float(value[0])],axis=0)

# fout.close()

# print("written to "+outfile+".dat")

# plotHistogram(data)
plotProbDensity(data)

# plt.plot(velArray,binArray)

print("DONE")



