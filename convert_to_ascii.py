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
p = OptionParser(usage="""usage: %prog [options] <fille_prefix> <start> <end>

Converts bindary files to ASCII format

<start>  starting file
<end>    finishing file
<file_prefix> either "out_0par" or "out_0disk"

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 3:
   p.print_help()
   sys.exit(1)
(file_prefix,start, end) = args

for no_of_files in range(int(start),int(end)):
  file_name = file_prefix+str(no_of_files)+".dat"
  f = open(file_name, 'rb')

  fout = open("_"+file_name, 'w')
  x = np.fromfile(f, dtype=np.float)  # read the data into numpy array


  size = len(x)/8

  if file_prefix == "out_0par":
    if opts.verbose:print "Writing particle file ",no_of_files
    index = 1
    for i in range(0,size):
      fout.write(str(x[index]*1e+3)+'\t'+str(x[index+1]*1e+3)+'\t'+str(x[index+2]*1e+3)
        +'\t'+str(x[index+3])+'\t'+str(x[index+4])+'\t'+str(x[index+5])+'\t'+str(x[index+6])+'\n')
      index += 8

  elif file_prefix == "out_0disk":
    if opts.verbose:print "Writing drum file ",no_of_files
    index = 2
    print x[0]
    print x[1]

    fout.write(str(int(x[0]))+'\n')
    for i in range(0,int(x[0])):
      fout.write(str(5*x[index]*1e+3)+'\t'+str(5*x[index+1]*1e+3)+'\t'+str(x[index+2]*1e+3)+'\n')
      index += 9

    for i in range(0,int(x[1])):
      fout.write(str(int(x[index]))+'\t'+str(int(x[index+1]))+'\t'+str(int(x[index+2]))+'\n')
      index += 3
  fout.close()
  f.close()

print "DONE"
