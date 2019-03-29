#!/tools/python/2.6-x86_64/bin/python

import numpy as np
import os
import sys
from optparse import OptionParser, OptionValueError

# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')



# parse command line
p = OptionParser(usage="""usage: %prog [options] <inputfile><zmin><zmax><outputfile>
Reads binary particle file <inputfile> and extract particle velocites only in the reagion defined by
lines y-x-20=0 and y-x+20=0 

Z constraints
<zmin> 
<zmax>


""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 4:
   p.print_help()
   sys.exit(1)
(in_file, zmin, zmax,out_file) = args


f = open(in_file, 'rb')
data = np.fromfile(f, dtype=np.float)  # read the data into numpy array

x=0
y=0
f1 = y-x-20
f2 = y-x+20
velocity_data = []

index = 1
count = 0

size = len(data)/8

for i in range(0,size):
  #fout.write(str(data[index]*1e+3)+'\t'+str(data[index+1]*1e+3)+'\t'+str(data[index+2]*1e+3)
#	+'\t'+str(data[index+3])+'\t'+str(data[index+4])+'\t'+str(data[index+5])+'\t'+str(data[index+6])+'\n')
  f1 = data[index+1]*1e+3-data[index]*1e+3-20
  f1 = data[index+1]*1e+3-data[index]*1e+3+20

  if data[index+2]*1e+3 > float(zmin) and data[index+1]*1e+3 < float(zmax):
    if f1<0 and f2>0 and data[index+6] < 5.5:
      count += 1
      r = np.sqrt((data[index]*1e+3)**2+(data[index+1]*1e+3)**2)
      velocity_data.append(str(count)+" "+str(r)+" "+str(data[index+6])+"\n")
#for i in range(0,int(x[0])):
  index += 8
#  fout.write(str(x[index]*1e+3)+'\t'+str(x[index+1]*1e+3)+'\t'+str(x[index+2]*1e+3)+'\n')
#  index += 8

f.close()


fout = open(out_file, 'w')
fout.writelines(velocity_data)
fout.close()

print "DONE"

