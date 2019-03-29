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
p = OptionParser(usage="""usage: %prog [options] <particle_smallest_diameter> <par_largest_diameter><total_np><drum_diameter><drum_length> <outputfile>

Construct MainClass.h and generate sample.dump


""")
p.add_option("-v", action="store_true",dest="verbose",  help="Verbose")
p.add_option("-s", action="store", dest="input_dump", type="str", help="read sample dump file")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 6:
   p.print_help()
   sys.exit(1)
(par_smallest_diameter,par_largest_diameter,total, drum_diameter,drum_length,out_file) = args

#### Mill parameters ##################
drum_diameter = float(drum_diameter)
drum_length = float(drum_length)
par_smallest_diameter = float(par_smallest_diameter)
par_largest_diameter = float(par_largest_diameter)
density = 7000.0
min_distance = int(1.5*par_largest_diameter)
no_of_particles = int(total)
rmax = int(drum_diameter*0.5 - par_largest_diameter)
zmin = int(par_largest_diameter)
zmax = int(drum_length - par_largest_diameter)

i_index = (int)(drum_diameter/(par_largest_diameter*1.55))
j_index = i_index
k_index = (int)(drum_length/(par_largest_diameter*1.55))

collGapCoeff = 0.1*1e-3
rIn = par_largest_diameter*1e-3
rOut = 1.55*par_largest_diameter*1e-3
allowedDistance = (rOut-rIn)/2.0
neighParListSize = 300
arraySz = 160
neighListArraySz = 160
gapAllowed = int(par_smallest_diameter)*0.10*1e-3 # 3% of the smallest particle diameter
largestParDensity = 7000.0

print "Drum diameter ",drum_diameter
print "Drum length ",drum_length
print "Cell indices ",i_index,j_index,k_index
fout = open(out_file, 'w')

##### Write mesh data ###############
dx = drum_diameter/i_index
dy = drum_diameter/j_index
dz = drum_length/k_index

print "dx,dy,dz ",dx,dy,dz

x_length = drum_diameter + 2*dx
y_length = drum_diameter + 2*dy
z_length = drum_length + 2*dz

print "x_length,y_length,y_length ",x_length,y_length,z_length

i_index += 2
j_index += 2
k_index += 2

dx = x_length/i_index
dy = y_length/j_index
dz = z_length/k_index

print "Modified dx,dy,dz ",dx,dy,dz

cell_no = 1

f = open("mesh_coords.dat", 'w')
for k in range(k_index):
  z = -0.5*dz + k*dz
  for j in range(j_index):
    y = -0.5*dy + j*dy
    for i in range(i_index):
      x = -0.5*dx + i*dx
      f.write(str(cell_no) +' '+str(x)+' '+str(y)+' '+str(z)+'\n')
      cell_no += 1

f.close()

cell_no = 1

f = open("mesh_neighbours.dat", 'w')
for k in range(k_index):
  for j in range(j_index):
    for i in range(i_index):
      if i > 0 and i < i_index-1 and j > 0 and j < j_index-1 and k > 0 and k < k_index-1:
        f.write(str(cell_no)+' ')
        for kk in range(k-1, k+2):
          for jj in range(j-1, j+2):
            for ii in range(i-1, i+2):
              p = ii;
              q = jj*i_index;
              r = kk*i_index*j_index;


              f.write(str(p+q+r+1)+' ')
        f.write('\n') 
      else:
        f.write(str(cell_no)+' 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1'+'\n') 
      cell_no += 1

f.close()



#exit(0)


##### Write parameters.h file #######
f_out = open("parameters.h",'w')

f_out.write("//------ Cell constants ------------------------------------------------------\n")
f_out.write("#define iIndex "+str(i_index)+"\n")
f_out.write("#define jIndex "+str(j_index)+"\n")
f_out.write("#define kIndex "+str(k_index)+"\n")
f_out.write("#define xLength "+str(x_length)+"\n")
f_out.write("#define yLength "+str(y_length)+"\n")
f_out.write("#define zLength "+str(z_length)+"\n")
f_out.write("//---------------------------------------------------------------------------\n")

f_out.write("//------ Particle constants ---------------------------------------------------\n")
f_out.write("#define particleArraySize "+str(no_of_particles+2)+"\n")
f_out.write("#define collGapCoeff 0.1*1e-3\n")
f_out.write("#define rIn "+str(rIn)+" //par diameter - largest particle\n")
f_out.write("#define rOut "+str(rOut)+" // rIn*1.55 - largest particle\n")
f_out.write("#define allowedDistance "+str(allowedDistance)+" // (rOut-rIn)/2 - smallest particle\n")
f_out.write("#define neighParListSize 300 //no particles in a cell\n")
f_out.write("#define arraySz 160 //particle contact list\n")
f_out.write("#define neighListArraySz 160 //neighbour list of a particle\n")
f_out.write("#define gapAllowed "+str(gapAllowed)+" //maximum allowed overlap\n")
f_out.write("#define largestParDia "+str(par_largest_diameter)+"\n")
f_out.write("#define largestParDensity "+str(largestParDensity)+"\n")
f_out.write("//------------------------------------------------------------------------------\n")

f_out.write("//----- Bonding parameters -----------------------------------------------------\n")
f_out.write("#define const_tensileStrength 1000\n")
f_out.write("#define const_shearStrength 1000\n")
f_out.write("//-----------------------------------------------------------------------------\n")
f_out.close()


######################################

#### Generate particles ##############
x = []
y = []
z = []
par_no = []
color = []
dia = []
dens = []
vel_x = []
vel_y = []
vel_z = []
omega_x = []
omega_y = []
omega_z = []

no_of_par = 0

if opts.input_dump: 
  print "Reading "+opts.input_dump
  f = open(opts.input_dump, 'r')
  data = f.readlines()
  f.close()

  line = data[5].strip()
  tuple = line.split()

  no_of_par = tuple[1]

  print no_of_par
  
  start = 8
  end = start+int(no_of_par)
  for i in range(start, end):
    line = data[i].strip()
    tuple = line.split()
    par_no.append(tuple[1])
    x.append(tuple[2])
    y.append(tuple[3])
    z.append(tuple[4])
    color.append(tuple[5])
    dia.append(tuple[6])
    dens.append(tuple[7])
    vel_x.append(tuple[8])
    vel_y.append(tuple[9])
    vel_z.append(tuple[10])
    omega_x.append(tuple[11])
    omega_y.append(tuple[12])
    omega_z.append(tuple[13])


print "rmax",rmax
print "zmin",zmin
print "zmax",zmax
print "min_distance",min_distance
insert = 1
count = int(no_of_par)

while (count < no_of_particles+1):
  insert = 1
  r = random.randint(int(par_largest_diameter),rmax)
  theta = random.randint(0,360)
  temp_z = random.randint(zmin,zmax)

  temp_x = r*math.cos(theta*math.pi/180.0)
  temp_y = r*math.sin(theta*math.pi/180.0)

  
  for i in range(len(x)):
    dist = math.sqrt((float(x[i])-temp_x)*(float(x[i])-temp_x) + (float(y[i])-temp_y)*(float(y[i])-temp_y) + (float(z[i])-temp_z)*(float(z[i])-temp_z))
    if (dist <  min_distance):
      insert = 0
      break

  if(insert == 1):
    par_no.insert(count,count+1)
    x.insert(count,temp_x)
    y.insert(count,temp_y)
    z.insert(count,temp_z)
    color.insert(count,0)
    dia.insert(count,par_smallest_diameter)
    dens.insert(count,density)
    vel_x.insert(count,0)
    vel_y.insert(count,0)
    vel_z.insert(count,0)
    omega_x.insert(count,0)
    omega_y.insert(count,0)
    omega_z.insert(count,0)
 
    count += 1

fout.write("SIMULATION TIME 0.0405\n")
fout.write("TIME\n")
fout.write("#\n")
fout.write("+ 0.0\n")
fout.write("#\n")
fout.write("np "+str(no_of_particles)+"\n")

fout.write("   Particle Position\n")
fout.write("#\n")

print "No of particles "+str(len(x)-1)
#exit(0)


for i in range(count-1):
  fout.write('+ '+str(par_no[i])+'\t'+str(x[i])+'\t'+str(y[i])+'\t'+str(z[i])+'\t'+str(color[i])+'\t'+str(dia[i])+'\t'+str(dens[i])+'\t'+str(vel_x[i])+'\t'+str(vel_y[i])+'\t'+str(vel_z[i])+'\t'+str(omega_x[i])+'\t'+str(omega_y[i])+'\t'+str(omega_z[i])+'\n')

fout.write("#\n")
fout.write("   Rotor angular position /(rad)\n")
fout.write("#\n")
fout.write("+ 0.000\n")
fout.write("#\n")


print "DONE"
fout.close()
