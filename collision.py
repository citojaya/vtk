#!/tools/python/2.6-x86_64/bin/python
from scipy.stats import f
from scipy.stats import skewnorm
#from matplotlib import pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
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

def plotNormDist(array, title, xlable):
  np.random.seed(0)

  # example data
  mu = 100  # mean of distribution
  sigma = 15  # standard deviation of distribution

  mu = np.mean(array)
  sigma = np.std(array,ddof=1)

  #x = mu + sigma * np.random.randn(437)

  #print(x)
  num_bins = 50

  fig, ax = plt.subplots()

  # the histogram of the data
  n, bins, patches = ax.hist(array, num_bins, normed=1)

  # add a 'best fit' line
  y = mlab.normpdf(bins, mu, sigma)
  
  ax.plot(bins, y, '--')
  ax.set_xlabel(xlable)
  ax.set_ylabel('Probability density')
  ax.set_title(title+': $\mu='+str(round(mu,2))+'$, $\sigma='+str(round(sigma,2))+'$')

  # Tweak spacing to prevent clipping of ylabel
  fig.tight_layout()
  plt.show()

def skewNormDist(array):
  a = 4
  fig, ax = plt.subplots(1, 1)
  mean, var, skew, kurt = skewnorm.stats(a, moments='mvsk')
  x = np.linspace(skewnorm.ppf(0.01, a),skewnorm.ppf(0.99, a), 100)
  ax.plot(x, skewnorm.pdf(x, a),'r-', lw=5, alpha=0.6, label='skewnorm pdf')

  r = skewnorm.rvs(a, size=1000)
  #ax.hist(array, normed=True, histtype='stepfilled', alpha=0.2)
  #ax.legend(loc='best', frameon=False)
  plt.show()

def plotHistogram(array, xLable, title, minVal, maxVal):
  print("Sample Standard Deviation ",np.std(array,ddof=1))
  print("Mean ",np.mean(array))

  size = 30
  binSize = (maxVal-minVal)/size
  
  print("Bin Size ",binSize)
  print("Min and Max ",minVal,maxVal)

  binArray = np.array([])
  for i in range(1,size+1):
    binArray = np.append(binArray, [minVal+binSize*i],axis=0)

  # hist,bins = np.histogram(array,binArray)
  plt.title(title)
  plt.ylabel("Frequency")
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

minX = 1000
with open(infile) as fin:
  for line in fin:
      if(line.split()[0] == "TIME"):
        count = 0
        blockCount += 1
        print("BLOCK ",blockCount)
       
      else:
        count += 1
        #print(line)
        minX = min(minX,float(line.split()[0]))
        xx = float(line.split()[0])
        if(xx >5):
          vx = float(line.split()[3])
          vy = float(line.split()[4])
          vz = float(line.split()[5])
          velMag = np.sqrt(vx*vx+vy*vy+vz*vz)
        # data[line.split()[11]] = [line.split()[7],line.split()[8],line.split()[9],line.split()[10],velMag,]
          data[line.split()[12]] = [line.split()[7],line.split()[8],line.split()[9],line.split()[10],velMag,line.split()[11]]
      
      if(int(frame)) == blockCount:
        break

print("minX ",minX)
val = 2
velArray = np.array([])
ppCollArray = np.array([])
pwCollArray = np.array([])
ppCollEArray = np.array([])
pwCollEArray = np.array([])
totalCollEArray = np.array([])
echargeArray = np.array([])

print("SIZE ",len(data))
fout = open(outfile+".dat","w")
for key,value in data.items():
  line = value[0]+" "+value[1]+" "+value[2]+" "+value[3]+" "+str(value[4])
  fout.write(str(key)+" "+line+"\n")
  echargeArray = np.append(echargeArray,[float(value[5])],axis=0)
  velArray = np.append(velArray,[float(value[4])],axis=0)
  ppCollArray = np.append(ppCollArray,[float(value[3])],axis=0)
  pwCollArray = np.append(pwCollArray,[float(value[2])],axis=0)
  ppCollEArray = np.append(ppCollEArray,[float(value[1])*1e-3],axis=0)
  pwCollEArray = np.append(pwCollEArray,[float(value[0])*1e-3],axis=0)
  totalCollEArray = np.append(totalCollEArray,[float(value[1])*1e-3+float(value[0])*1e-3],axis=0)

fout.close()

print("written to "+outfile+".dat")

#plotHistogram(ppCollArray, "Number of impacts","Particle-Particle Collisions",min(ppCollArray),max(ppCollArray))
#plotHistogram(pwCollArray, "Number of impacts","Particle-Wall Collisions")
# plotHistogram(ppCollEArray, "Collision Energy (1e-9 J)", "Particle-Particle Collision Energy")
# plotHistogram(pwCollEArray)
#plotHistogram(velArray, "Velocity (m/s)", "Velocity Distribution",min(velArray),max(velArray))
# plotHistogram(totalCollEArray,"Collision Energy (1e-9 J)","Collision Energy Distribution")
plotHistogram(echargeArray,"Electric Charge","Electric Charge Distribution",min(echargeArray),max(echargeArray))
#plotNormDist(velArray, 'Velocity Normal Distribution', 'Velocity (m/s)')
# plotHistogram(echargeArray, 'Charge Normal Distribution', 'Charge (C)')
#skewNormDist(velArray)
# plt.plot(velArray,binArray)


print("DONE")



