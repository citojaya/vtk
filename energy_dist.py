#!/tools/python/2.6-x86_64/bin/python
import pylab
import numpy as np
import os
import sys
import math
from optparse import OptionParser, OptionValueError

# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')



# parse command line
p = OptionParser(usage="""usage: %prog [options] <sim_time>

<sim_time> simulation time

Reads binary "out_particleForce.dat"  and produce following energy distribution files

histresultant_energy.dat
hist_norm_energy.dat
hist_tang_energy.dat

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 1:
   p.print_help()
   sys.exit(1)
(division) = args[0]


if opts.verbose: print "Reading out_particleForce.dat"
f = open("out_particleForce.dat", 'rb')
#fout = open(out_file, 'w')
x = np.fromfile(f, dtype=np.float)  # read the data into numpy array
f.close()


index = 0

size = len(x)/8

norm_energy = []
tang_energy = []
resultant_energy = []

normal_collisions = 0
tangential_collisions = 0

if opts.verbose: print "Calculating histograms"
for i in range(0,size):
  # particle-particle collisions
  if float(x[index]) > 0:
  # x[index+4] is normal energy
    if float(x[index+4]) > 1e-7 and float(x[index+4]) < 0.009:
      norm_energy.append(float(x[index+4]))
      normal_collisions += 1
    # x[index+5] is tangential energy
    if float(x[index+5]) > 1e-7 and float(x[index+5]) < 0.001:
      tang_energy.append(float(x[index+5]))
      tangential_collisions += 1

    #resultant = math.sqrt(float(x[index+4])*float(x[index+4])+float(x[index+5])*float(x[index+5]))
    resultant = float(x[index+4])+float(x[index+5])
    #if float(x[index+5]) > 1e-7 and float(x[index+5]) < 0.001:
    #  tang_energy.append(float(x[index+5]))

    if resultant > 1e-7 and resultant <0.009:
      resultant_energy.append(resultant)

    #fout.write(str(x[index])+'\t'+str(x[index+4])+'\t'+str(x[index+5])+'\n')
  index += 8
#fout.close()

#exit(0)

minval = min(norm_energy)
maxval = max(norm_energy)

print "MIN and MAX energy ",minval,maxval
print "Total normal collisons "+str(normal_collisions)
print "Total tangential collisons "+str(tangential_collisions)

# Frequency distribution
#bin = [-1,10,20,30,40,50,60,70,80,90,100]
#hist = pylab.hist(no_of_coll, 14, normed=True)
norm_hist = pylab.hist(norm_energy, 1000)
tang_hist = pylab.hist(tang_energy, 1000)
resultant_hist = pylab.hist(resultant_energy, 1000)
#hist = np.histogram(no_of_coll, bin)
norm_y = norm_hist.__getitem__(0)
norm_x = norm_hist.__getitem__(1)

tang_y = tang_hist.__getitem__(0)
tang_x = tang_hist.__getitem__(1)

res_y = resultant_hist.__getitem__(0)
res_x = resultant_hist.__getitem__(1)

f = open("hist_norm_energy.dat", 'w')
for i in range(0, norm_x.__len__()-1):
  f.write(str(norm_x[i])+'\t'+str(norm_y[i]/float(division))+'\n')
f.close()

f = open("hist_tang_energy.dat", 'w')
for i in range(0, tang_x.__len__()-1):
  f.write(str(tang_x[i])+'\t'+str(tang_y[i]/float(division))+'\n')
f.close()

f = open("hist_resultant_energy.dat", 'w')
for i in range(0, res_x.__len__()-1):
  f.write(str(res_x[i])+'\t'+str(res_y[i]/float(division))+'\n')
f.close()

print "DONE"

