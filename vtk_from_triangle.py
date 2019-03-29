#!/tools/python/2.6-x86_64/bin/python

import os
import sys
#import subprocess
import re
from optparse import OptionParser, OptionValueError

import numpy as np
#import scipy.linalg
import glob
import vtk
from vtk.util import numpy_support

# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')

# parse command line
# parse command line
p = OptionParser(usage="""usage: %prog [options] <input.dat>  <out_vtu> 

Generates 3D mesh based on triangular mesh data
<input.dat> - triangulate mesh data in the following format

no_of_data_points
x1 y1 z1
x2 y2 z2
.......
.......
p1 p2 p3
.......

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")
p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, .vtu output")
(opts, args) = p.parse_args()


# Get the arguments

if len(args) == 1:
  (filename) = args[0]

else:
   p.print_help()
   sys.exit(1)

nodes = []
nodes_array = vtk.vtkIntArray()
nodes_array.SetName("nodes")
node_x = []
node_y = []
node_z = []

connect_1 = []
connect_2 = []
connect_3 = []

point = vtk.vtkPoints()

counter = 1

output = vtk.vtkUnstructuredGrid()

# Read nod files
if opts.verbose: print "Reading "+filename+" data file"
infile = open(filename, 'r')

no_of_points = int(infile.readline())

# print(no_of_points)
# exit(0)

# dictionary to store neighbour nodes
node = {}


for i in range(no_of_points):
  line  = infile.readline()
  tuple = line.split()

  nodes_array.InsertNextValue(counter)
  nodes.append(counter)
  node_x.append(round(float(tuple[0])*1e3,3)) #units in mm
  node_y.append(round(float(tuple[1])*1e3,3))
  node_z.append(round(float(tuple[2])*1e3,3))

  node[counter] = [] #neighbour node list
  counter += 1
  

counter = 0
#print(len(node[0]))

for line in infile:
  if not line.split():
    continue
  tuple = line.split()
  connect_1.append(int(tuple[0]))
  connect_2.append(int(tuple[1]))
  connect_3.append(int(tuple[2]))

  # Build neighbouring node list which is used for surface contact detection 
  node[int(tuple[0])].append(int(tuple[1]))
  node[int(tuple[0])].append(int(tuple[2]))
  node[int(tuple[1])].append(int(tuple[0]))
  node[int(tuple[1])].append(int(tuple[2]))
  node[int(tuple[2])].append(int(tuple[0]))
  node[int(tuple[2])].append(int(tuple[1]))

  counter += 1

infile.close()

#write node coordinates and connectivity 
f = open(filename[:-4]+"_nodes.dat", "w")

for i in range(no_of_points):
  f.write(str(node_x[i])+" "+str(node_y[i])+" "+str(node_z[i])+" "+str(len(node[i+1])))
  for j in range(len(node[i+1])):  
    f.write(" "+str(node[i+1][j]))
    
  f.write("\n")

f.close()

#print counter
# for i in range(no_of_points):
#   if(len(node[i+1]) < 5):
#     print len(node[i+1])
#print connect_1[0]
#print connect_1[4]

#exit(0)

for i in range(0,no_of_points):
  point.InsertNextPoint(round(float(node_x[i]),3),round(float(node_y[i]),3),round(float(node_z[i]),3))

 
output.SetPoints(point)
output.GetPointData().AddArray(nodes_array)
#layer = []
#cell = []
 
layer_array = vtk.vtkStringArray()
cell_array = vtk.vtkIntArray()
cell_array.SetName("cell")


# List of .ele files


for i in range(counter):

  #layer.append(tuple[0])
  #cell.append(tuple[1])

  #layer_array.InsertNextValue((tuple[0]))
  cell_array.InsertNextValue(i+1)
  triangle = vtk.vtkTriangle().GetPointIds()
  triangle.SetId(0, int(connect_1[i])-1)
  triangle.SetId(1, int(connect_2[i])-1)
  triangle.SetId(2, int(connect_3[i])-1)
# Enter 5 for triangle
  output.InsertNextCell(5, triangle)



output.GetCellData().AddArray(cell_array)


command_used = vtk.vtkStringArray()
command_used.SetName("provenance")
command_used.InsertNextValue(" ".join(sys.argv))
output.GetFieldData().AddArray(command_used)


# Write output file
out_file = filename[:-3]+"vtu"
if opts.verbose: print "Writing", out_file
writer = vtk.vtkXMLUnstructuredGridWriter()
writer.SetFileName(out_file)


if opts.ascii:
   writer.SetDataModeToAscii()
else:
   writer.SetDataModeToBinary()

writer.SetInputData(output)
#writer.SetInputConnection(output.GetProducerPort())
writer.Write()
