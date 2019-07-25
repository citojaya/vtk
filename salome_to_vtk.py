#!/usr/bin/env python

import vtk
import os
import sys
import re
import glob
import math
from optparse import OptionParser, OptionValueError

arrSize = 1500

# parse command line
p = OptionParser(usage="""usage: %prog [options] <salome-mesh>

Read SALOME mesh file (triangular mesh only) and write to output which will be used to generate
VTK file. 

<salome-mesh> - SALOME mesh file 
Ex: salome_to_vtk.py wall (input file is wall.mesh)

""")


p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")
#p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, VTK output")
(opts, args) = p.parse_args()

if len(args) < 1:
   print 'check input and output files'
   sys.exit(0)
(file_name) = args[0]

#mesh_files = glob.glob("*.mesh")
#padit = int(math.log10(len(mesh_files))+1)

#print padit
#sys.exit(0)

if opts.verbose:print"Reading salome mesh file"
edges = False
vertices = False
triangle = False
vertices_data = []
triangles_data = []
edges_data = []

f = open(file_name, "r")
for line in f:
  if not line.split():
    continue
  tuple = line.split()
  
  if vertices:
    vertices_data.append(line)
  if triangle:
    triangles_data.append(line)
  if edges:
    edges_data.append(line)

  if tuple[0] == "Vertices":
    vertices = True
    edges = False
  if tuple[0] == "Edges":
    edges = True
    vertices = False
  if tuple[0] == "Triangles":
    triangle = True
  if tuple[0] == "End":
    triangle = False

f.close()

scale = 1.0 #scale factor for coordinates
f = open(file_name[:-5]+".dat","w")
f.write(str(vertices_data[0].strip())+"\n")
for i in range(1,int(vertices_data[0])+1):
  tuple = vertices_data[i].split()
  f.write(str(round(float(tuple[0])*scale,6))+" "+str(round(float(tuple[1])*scale,6))+" "+str(round(float(tuple[2])*scale,6))+"\n")

for i in range(1,int(triangles_data[0])+1):
  tuple = triangles_data[i].split()
  f.write(tuple[0]+" "+tuple[1]+" "+tuple[2]+"\n")
f.close()

# Write triangular faces for CFD

f = open("wall-mesh.dat","w")
f.write(str(int(triangles_data[0]))+"\n")
#go through triangle surfaces
for i in range(1,int(triangles_data[0])+1):
  tuple = triangles_data[i].split()
  # Get node coordinates
  tuple = triangles_data[i].split()
  nd1 = tuple[0]
  nd2 = tuple[1]
  nd3 = tuple[2]
  
  tuple1 = vertices_data[int(nd1)].split()
  tuple2 = vertices_data[int(nd2)].split()
  tuple3 = vertices_data[int(nd3)].split()

  x1 = str(round(float(tuple1[0]),6))
  y1 = str(round(float(tuple1[1]),6))
  z1 = str(round(float(tuple1[2]),6))

  x2 = str(round(float(tuple2[0]),6))
  y2 = str(round(float(tuple2[1]),6))
  z2 = str(round(float(tuple2[2]),6))

  x3 = str(round(float(tuple3[0]),6))
  y3 = str(round(float(tuple3[1]),6))
  z3 = str(round(float(tuple3[2]),6))

  line = " ".join([x1,y1,z1,x2,y2,z2,x3,y3,z3])
  f.write(line+"\n")

f.close()

# Write connectivity file for CFD
coords = vertices_data
connectivity = [[] for x in range(len(vertices_data))]
  
# Read cells and connectivity
for i in range(1,int(triangles_data[0])+1):
  tuple = triangles_data[i].split()
  id1 = int(tuple[0])
  id2 = int(tuple[1])
  id3 = int(tuple[2])
  if(id2 not in connectivity[id1]):
    connectivity[id1].append(id2)
  if(id3 not in connectivity[id1]):  
    connectivity[id1].append(id3)
  
  if(id1 not in connectivity[id2]):
    connectivity[id2].append(id1)
  if(id3 not in connectivity[id2]):
    connectivity[id2].append(id3)
  if(id1 not in connectivity[id3]):
    connectivity[id3].append(id1)
  if(id2 not in connectivity[id3]):
    connectivity[id3].append(id2)
    
f = open("mesh_connect.dat","w")
f.write(str(vertices_data[0]))
f.write(str(triangles_data[0]))
for i in range(1,int(vertices_data[0])+1):
  tuple = vertices_data[i].split()
  f.write(str(round(float(tuple[0])*scale,3))+" "+\
    str(round(float(tuple[1])*scale,3))+" "+\
    str(round(float(tuple[2])*scale,3))+" "+str(len(connectivity[i]))+" ")
  for j in range(len(connectivity[i])):
    f.write(str(connectivity[i][j])+" ")
  f.write("\n")

f.close()

print "DONE"

