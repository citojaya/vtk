#!/tools/python/2.6-x86_64/bin/python
import numpy as np
import os
import random
import math
import sys
import library.vtk_tools as vtk_t
import glob

from optparse import OptionParser, OptionValueError



# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')


# parse command line:
p = OptionParser(usage="""Program <start> <end> <angVel>

Read capsule mesh and genrate separate files for rotation 
<infile> capsule mesh file
<angVel> angular velocity in rad/s
<steps> - number of steps to be generated


""")
p.add_option("-v", action="store_true",   dest="verbose",  help="Verbose")
p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, .vtu output")
p.add_option("-s", action="store", dest="input_dump", type="str", help="read sample dump file")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 3:
   p.print_help()
   sys.exit(1)
(infile, angVel, steps) = args

dt = 1.e-4

f = open(infile,"r")
nF = f.readline()
interval = 1
# print(nF)
nodes = []
omega = -float(angVel)*dt*interval
for i in range(int(nF)):
    line = f.readline()
    # print(line)
    nodes.append(line)

connect = []
while(line.split()):
    line = f.readline()
    connect.append(line)
    # print(line)

f.close()

yShift = 0.003
zShift = -0.003
for n in range (int(steps)):
    outfile = infile[:-9]+str(n+1)+".dat"
    print(outfile)
    f = open(outfile,"w")
    f.write(str(nF))
    for i in range(len(nodes)):
        tuple = nodes[i].split()
        
        xx = float(tuple[0])
        yy = float(tuple[1]) + yShift
        zz = float(tuple[2]) + zShift
        
        newX = xx*np.cos(omega*(n+1))-zz*np.sin(omega*(n+1))
        newY = yy 
        newZ = xx*np.sin(omega*(n+1))+zz*np.cos(omega*(n+1)) 
        
        newLine = " ".join([str(round(newX,6)),str(round(newY,6)),str(round(newZ,6))])
        f.write(newLine+"\n")

    for i in range(len(connect)):
        f.write(connect[i])
    f.close()

print ("DONE") 

