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
p = OptionParser(usage="""Program <start> <end>

<start> - starting file
<end> - finishing file

Call following scirpts
./vtk_from_triangle.py - Read triangulate mesh file which contains information of the drum and convert to vtu format



""")
p.add_option("-v", action="store_true",        dest="verbose",  help="Verbose")
p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, .vtu output")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 1:
   p.print_help()
   sys.exit(1)
(prefix) = args[0]



# Read esys output fils
list_of_files_dict = {}
list_of_files = glob.glob(prefix+"_t="+"*"+"_1.txt")
for filename in list_of_files:
  file_no = filename[len(prefix)+3:-6]
  list_of_files_dict[int(file_no)]=filename

keylist = list_of_files_dict.keys()
keylist.sort()


no_of_files = 0
for key in keylist:
  no_of_files += 1
  filename = list_of_files_dict[key]

  if opts.verbose:print "Writing file",filename
  f = open(filename, 'r')
  data = f.readlines()
  f.close()

  no_of_nodes = 0
  mesh_data = []
  read_nodes = False 
  counter = 0
  read_tri = False
  counter2 = 0
  no_of_tri = 0
  for i in range(len(data)):
    tuple = data[i].split()
    
    if read_nodes:
      line = tuple[3]+" "+tuple[4]+" "+tuple[5]+"\n"
      mesh_data.append(line)
      counter += 1

    if read_tri:
      line = tuple[2]+" "+tuple[3]+" "+tuple[4]+"\n"
      mesh_data.append(line)
      counter2 += 1

    if tuple[0] == "3D-Nodes":
      no_of_nodes =int(tuple[1])
      read_nodes = True  
      mesh_data.append(str(no_of_nodes)+"\n")
    if counter == no_of_nodes:
      read_nodes = False

    if tuple[0] == "Tri3":
      no_of_tri =int(tuple[1])
      read_tri = True

    if counter2 == no_of_tri:
      read_tri = False
  
  f = open(filename[:-3]+"mesh","w")
  f.writelines(mesh_data)
  f.close()
# List of vtu files
  fileNames = []

#for no_of_files in range(int(start),int(end)):
  #file_name = "out_0disk"+str(no_of_files)+".dat"
  #os.system("read_binary_drum.py "+file_name+" "+"ascii_"+file_name)
  
  os.system("vtk_from_triangle.py "+filename[:-3]+"mesh "+filename[:-3]+"vtu")
  
  fileNames.append(filename[:-3]+"vtu")

#fileNames = glob.glob("out_0disk*.vtu")

#outFile = open("drum.pvd", 'w')

import xml.dom.minidom

pvd = xml.dom.minidom.Document()
pvd_root = pvd.createElementNS("VTK", "VTKFile")
pvd_root.setAttribute("type", "Collection")
pvd_root.setAttribute("version", "0.1")
pvd_root.setAttribute("byte_order", "LittleEndian")
pvd.appendChild(pvd_root)

collection = pvd.createElementNS("VTK", "Collection")
pvd_root.appendChild(collection)

for i in range(len(fileNames)):
  dataSet = pvd.createElementNS("VTK", "DataSet")
  dataSet.setAttribute("timestep", str(i))
  dataSet.setAttribute("group", "")
  dataSet.setAttribute("part", "0")
  dataSet.setAttribute("file", str(fileNames[i]))
  collection.appendChild(dataSet)

outFile = open("drum.pvd", 'w')
pvd.writexml(outFile, newl='\n')
outFile.close()



print "DONE" 

