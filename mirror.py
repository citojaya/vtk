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
p = OptionParser(usage="""usage: %prog [options] <in_dump> <out_dump>

Read in_dump and generate mirror image of particles and written to out_dump 


""")
p.add_option("-v", action="store_true",dest="verbose",  help="Verbose")
p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, .vtu output")
p.add_option("-s", action="store", dest="input_dump", type="str", help="read sample dump file")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 2:
   p.print_help()
   sys.exit(1)
(in_file, out_file) = args

f = open(in_file, 'r')
data = f.readlines()
f.close()

line = data[5].strip()
tuple = line.split()

no_of_par = int(tuple[1])

tuple[1] = str(2*no_of_par)

line = ' '.join(tuple)

data[5] = line+'\n'

#exit(0)

y_cutoff = -20.0

data_out = []

for i in range(data.__len__()):
  if i < 8+no_of_par:
    data_out.append(data[i])
  

for i in range(data.__len__()):
  if i > 7 and i <(8+no_of_par):
    line =  data[i].strip()
    tuple  = line.split()

    y_coord = float(tuple[3])
   
    if y_coord < y_cutoff:
      tuple[1] = str(int(tuple[1])+no_of_par)
      tuple[3] = str(-1.0*float(tuple[3]))
      tuple[8] = "0.0"
      tuple[9] = "0.0"
      tuple[10] = "0.0"
      tuple[11] = "0.0"
      tuple[12] = "0.0"
      tuple[13] = "0.0"
      #tuple[14] = "0.0"

      line = ' '.join(tuple)

      data_out.append(line+'\n')



  elif i > 7+no_of_par:
    data_out.append(data[i])

fout = open(out_file, 'w')
fout.writelines(data_out)
fout.close()






