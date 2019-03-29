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
p = OptionParser(usage="""usage: %prog [options] <start><end><time_step>
Read out_0par*.dat from start to end and calculate particle-particle collision 
frequnecy vs time and written to "collisions_vs_time.dat"

<start> starting file
<end> ending file
<time_step> time interval between two files


""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 3:
   p.print_help()
   sys.exit(1)
(start, end, time_interval) = args

start_file = int(start)
end_file = int(end)

time = []
coll_freq = []
count = 1
total_no_of_collisions = 0

for i in range(start_file, end_file):
  if opts.verbose: print "Reading file ",str(i)
  f = open("out_0par"+str(i)+".dat", 'rb')
  x = np.fromfile(f, dtype=np.float)  # read the data into numpy array
  f.close()

  index = 0

  size = len(x)/8

  prev_total_no_of_collisions = 0
  #no_of_coll = []
  # Write ASCII file
  for i in range(0,size):
    #no_of_coll.append(int(x[index+6]))
    total_no_of_collisions += int(x[index+6])
    #fout.write(str(x[index]*1e+3)+'\t'+str(x[index+1]*1e+3)+'\t'+str(x[index+2]*1e+3)
        #+'\t'+str(x[index+3])+'\t'+str(x[index+4])+'\t'+str(x[index+5])+'\t'+str(x[index+6])+'\n')
    index += 8

  total_no_of_collisions = total_no_of_collisions/(10.0)
  time.append(str(count*float(time_interval)))
  coll_freq.append(str((total_no_of_collisions-prev_total_no_of_collisions)/float(time_interval)))

  prev_total_no_of_collisions = total_no_of_collisions
  count += 1

f = open("collisions_vs_time.dat", "w")
for i in range(len(time)):
  f.write(str(time[i])+" "+str(coll_freq[i])+'\n')

f.close()

print "DONE"

