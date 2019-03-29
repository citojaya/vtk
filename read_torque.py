#!/tools/python/2.6-x86_64/bin/python

import numpy as np
import os
import random
import math
import sys

from optparse import OptionParser, OptionValueError



# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')


# parse command line
p = OptionParser(usage="""usage: %prog [options] <torquefile> <speed>

Filter out torque values between min and max and written to filtered_power.dat

<torquefile> torque file
<speed> mill speed in rpm
<min>  minimum value
<max>  maximu value

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")
p.add_option("--min", action="store", type="float", dest="minimum",  help="Torque values less than this value will be ignored", default="-10000")
p.add_option("--max", action="store", type="float", dest="maximum",  help="Torque values greater than this value will be ignored", default="10000")


(opts, args) = p.parse_args()
# get the com filename
if len(args) != 2:
   p.print_help()
   sys.exit(1)
(torquefile,speed) = args

f = open(torquefile, "r")
data = f.readlines()
f.close()

outfile = open("filtered_power.dat", "w")

average_power = 0.0
count = 0

for i in range(len(data)):
  line = data[i].strip()
  tuple = line.split()
  pwr = float(tuple[1])*2.0*math.pi*float(speed)/60.0
  if pwr > float(opts.minimum) and pwr < float(opts.maximum):
    #time = float(tuple[0])+i*0.001
    time = float(tuple[0])
    outfile.write(str(time)+" "+str(pwr)+" "+'\n')
    count += 1
    average_power += float(tuple[1])*2.0*math.pi*float(speed)/60.0

outfile.close()

print "Average power (W) ",str(average_power/count)
print "DONE"
