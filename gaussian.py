#!/tools/python/2.6-x86_64/bin/python
from pylab import *
import numpy as np
import numpy.random
import os
import random
import math
import sys
from optparse import OptionParser, OptionValueError



# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')


# parse command line
p = OptionParser(usage="""usage: %prog [options] <x_min> <x_max> <mean> <st_dev> <outfile> 
Writes normal distribution to <outfile>


""")
p.add_option("-v", action="store_true",        dest="verbose",  help="Verbose")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 5:
   p.print_help()
   sys.exit(1)
(x_min, x_max, mean, st_dev,  out_file) = args


def gauss(mu, sigma, x ) :
    return (1.0/(sigma*sqrt(2*pi)))*exp(-(x-mu)**2/(2.0*sigma**2))


# plot a normal distribution
x = arange(4, 16, 0.5 )
y = gauss( 10.0, 3.0, x )

print x
print y

f = open(out_file, 'w')
for i in range(len(x)):
  f.write(str(x[i])+' '+str(y[i])+'\n')

f.close() 

#plot(x,y)
#xlim(-4,4)

print "DONE"
