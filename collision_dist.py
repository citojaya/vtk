#!/tools/python/2.6-x86_64/bin/python
import pylab
import numpy as np
import os
import sys
from optparse import OptionParser, OptionValueError

# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')



# parse command line
p = OptionParser(usage="""usage: %prog [options] <inputfile> <outputfile>

Reads binary file and written to ASCII outputfile 
Calculate collision frequency distribution

<inputfile> out_0par*.dat
<outfile> output file

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 2:
   p.print_help()
   sys.exit(1)
(in_file, out_file) = args


f = open(in_file, 'rb')
fout = open(out_file, 'w')
x = np.fromfile(f, dtype=np.float)  # read the data into numpy array



index = 0

size = len(x)/8

no_of_coll = []
# Write ASCII file
for i in range(0,size):
  if int(x[index+6]) > 0:
    no_of_coll.append(int(x[index+6]))
  fout.write(str(x[index])+'\t'+str(x[index+1]*1e+3)+'\t'+str(x[index+2]*1e+3)+'\t'+str(x[index+3]*1e+3)
	+'\t'+str(x[index+4])+'\t'+str(x[index+5])+'\t'+str(x[index+6])+'\t'+str(x[index+7])+'\n')
  index += 8
fout.close()

minval = min(no_of_coll)
maxval = max(no_of_coll)

print minval,maxval

# Frequency distribution
#bin = [-1,10,20,30,40,50,60,70,80,90,100]
#hist = pylab.hist(no_of_coll, 14, normed=True)
hist = pylab.hist(no_of_coll, 20)
#hist = np.histogram(no_of_coll, bin)
y = hist.__getitem__(0)
x = hist.__getitem__(1)

f.close()
fout.close()

f = open("histogram_collision.dat", 'w')
for i in range(0, x.__len__()-1):
  f.write(str(x[i])+'\t'+str(y[i])+'\n')
f.close()
print "DONE"

