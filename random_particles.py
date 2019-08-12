#!/usr/bin/env python

#import vtk
import random
import os
import sys
import re
import glob
import math
import numpy as np
from optparse import OptionParser, OptionValueError

arrSize = 1500

# parse command line
p = OptionParser(usage="""usage: %prog [options] <particle diameter> <no of particles>

Generate random particles within a given domain
Alos this script can be used to copy injection file, convert big particles to micro etc

python random_particles.py <diameter>

""")

def orderedList():
    minX = minY = minZ = 100000
    maxX = maxY = maxZ = -100000

    parX = []
    parY = []
    parZ = []

    if opts.verbose:print ("Generating random particles\n")

    xDiv = 35 #max 49
    yDiv = 6  #max 8
    zDiv = 20 #35

    xShift = 102
    yShift = -4
    zShift = -47 #47

    no_of_part = 0

    gap = float(dia)*0.12
    print(xDiv,yDiv,zDiv)
    for k in range(zDiv):
        z = k*float(dia)+gap
        if(z < minZ):
            minZ = z
        if(z > maxZ):
            maxZ = z
        parZ.append(z)
        for j in range(yDiv):
            y = j*float(dia)+gap
            if(y < minY):
                minY = y
            if(y > maxY):
                maxY = y
            parY.append(y)
            for i in range(xDiv):
                x = i*float(dia)+gap
                if(x < minX):
                    minX = x
                if(x > maxX):
                    maxX = x
                parX.append(x)
                no_of_part += 1   
    print("MIN MAX ",minX+xShift,maxX+xShift,minY+yShift,maxY+yShift,minZ+zShift,maxZ+zShift)           
    print("Number of particles generated ",no_of_part,"\n")

    if opts.verbose:print ("Writing to injection file initial.inj")
    f = open("random.inj","w")
    #f.write(str(len(vertices_data))+"\n")

    for k in range(zDiv):
        for j in range(yDiv):
            for i in range(xDiv):
                sx = str(round((parX[i]+xShift)*1e-3,6))
                sy = str(round((parY[j]+yShift)*1e-3,6))
                sz = str(round((parZ[k]+zShift)*1e-3,6))
                sd = str(round(float(dia)*1e-3,4))
                # s = " ".join(str(round(parX[i]*1e-3,4)))
                # if(parZ[k]+zShift > 25 and parZ[k]+zShift < 45):
                f.write("(("+sx+" "+sy+" "+sz+" 0.0 0.0 0.0 "+sd+" 0.0 1.0))\n")
                # no_of_part  += 1
                # f.write("(("+str(round(parX[i]*1e-3,4))+" "+str(parY[j])+" "+str(parZ[k])+" 0.0 0.0 0.0 "+str(float(dia)*1e-3)+" 0.0 1.0))\n")
    f.close()

def distance(px,py,pz,px2,py2,pz2):
    dist = np.sqrt(np.power((float(px)-float(px2)),2)+np.power((float(py)-float(py2)),2)+np.power((float(pz)-float(pz2)),2))
    return dist

def insertable(px,py,pz,dia,particle):
    for x in range(len(particle)):
        (px2,py2,pz2) = particle[x]
        if(distance(px,py,pz,px2,py2,pz2) < float(dia)*1.02): 
            return False
        # if(float(px) == float(px2) and float(py) == float(py2) and float(pz) == float(pz2)):
        #     return False
    return True
 
def randomList(parts,xmin,xmax,ymin,ymax,zmin,zmax,centDist,dmin,dmax):
    xMin = 1000
    yMin = 1000
    zMin = 1000
    xMax = -1000
    yMax = -1000
    zMax = -1000

    particle = []
    noOfParts = 0
    xdiv = (int)((xmax-xmin)/centDist)
    ydiv = (int)((ymax-ymin)/centDist)
    zdiv = (int)((zmax-zmin)/centDist)
    print("xdiv, ydiv, zdiv",xdiv,ydiv,zdiv)

    if opts.verbose:print ("Writing to injection file initial.inj")
    f = open("initial.inj","w")
    fp = open("particle.dat","w")
    fp.write("TIME = 0.0\n")
    while(noOfParts < int(parts)):
        px = random.randint(xmin,xmax)*0.01
        py = random.randint(ymin,ymax)*0.01
        pz = random.randint(zmin,zmax)*0.01
        randSize = random.randint(int(dmin), int(dmax))*0.01
        # if(insertable(px,py,pz,dia,particle)):
        center = np.array([0,0,pz])
        p = np.array([px,py,pz])
        # r = np.sqrt(px*px+pz*pz)
        r = np.linalg.norm(p - center)
        if(r > 7.8 and r < 8.4):
           if(insertable(px,py,pz,randSize,particle)):
                px1 = str(round(px,6))
                py1 = str(round(py,6))
                pz1 = str(round(pz,6))
                pd = str(round(float(randSize),6))
                sx = str(round((px)*1e-3,6))
                sy = str(round((py)*1e-3,6))
                sz = str(round((pz)*1e-3,6))
                # size = str(round(float(dia)*1e-3,6))
                size = str(round(float(randSize)*1e-3,6))
                xMin = min(xMin,px)
                yMin = min(yMin,py)
                zMin = min(zMin,pz)
                xMax = max(xMax,px)
                yMax = max(yMax,py)
                zMax = max(zMax,pz)

                f.write("(("+sx+" "+sy+" "+sz+" 0.0 0.0 0.0 "+size+" 0.0 1.0))\n")
                line = " ".join([px1,py1,pz1,"0 0 0",pd,"0 0 0 0 0",str(noOfParts)])
                fp.write(line+"\n")
                particle.append((px,py,pz))
                noOfParts += 1
                if(noOfParts%100 == 0):
                    print("No of particles",noOfParts)

    # print("No of particles",noOfParts)
    print("Min Max",xMin,xMax,yMin,yMax,zMin,zMax)
    fp.close()
    f.close()
    # print(particle)

def shift(infile, outfile):
    
    zshift = 0.0
    # zshift = 0.0 #0.030
    #zshift = 0.004
    #zshift = 0.005
    #zshift = 0.006
    
    
    #xshift = 4.e-3 + 0.010e-3 - 0.014296
    xshift = -0.095
    xMax = -1.0
    xMin = 1.0e5
    f1 = open(infile, "r")
    f2 = open(outfile, "w")
    for line in f1:
        tuple = line.split()
        firststr = tuple[0]
        xx = float(firststr[2:]) + xshift
        xMax = max(xx,xMax)
        xMin = min(xMin,xx)
        yy = tuple[1]
        zz = float(tuple[2])
        zz += zshift
        zz = str(round(zz,6))

        # f2.write(line)
        f2.write("(("+str(round(xx,6))+" "+yy+" "+zz+" 0.0 0.0 0.0 "+tuple[6]+" 0.0 1.0))\n")
        #print (xx[2:],yy,str(zz))


    f1.close()
    f2.close()
    print("xMin ",xMin)
    print("xMax ",xMax)
    

def haircut(infile, outfile, val):
    f1 = open(infile, "r")
    f2 = open(outfile, "w")
    minVal = 1.0e3
    maxVal = -1.0e3
    for line in f1:
        tuple = line.split()
        firststr = tuple[0]
        xx = float(firststr[2:])
        yy = float(tuple[1])
        zz = float(tuple[2])
#        maxVal = max(maxVal,yy)
#        minVal = min(minVal,yy)
        #f2.write(line)
        if(yy > val):
          maxVal = max(maxVal,yy)
          minVal = min(minVal,yy)
          f2.write("(("+str(round(xx,6))+" "+str(round(yy,6))+" "+str(round(zz,6))+" 0.0 0.0 0.0 "+tuple[6]+" 0.0 1.0))\n")
        #print (xx[2:],yy,str(zz))

    f1.close()
    f2.close()
    print("minVal ",minVal)
    print("maxVal ",maxVal)

def convertToMicro(infile, outfile, scale):
    
    f1 = open(infile, "r")
    f2 = open(outfile, "w")
    for line in f1:
        tuple = line.split()
        firstStr = tuple[0]
        xx = float(firstStr[2:])*scale
        yy = float(tuple[1])*scale
        zz = float(tuple[2])*scale
        
        #zz = str(round(zz,6))
        dia = float(tuple[6])*scale

        f2.write("(("+str(round(xx,6))+" "+str(round(yy,6))+" "+str(round(zz,6))+" 0.0 0.0 0.0 "+str(round(dia,6))+" 0.0 1.0))\n")
        #print ("(("+str(round(xx,2)),str(round(yy,6)),str(zz),str(dia))

    f1.close()
    f2.close()

p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")
#p.add_option("-t", "--type",action="store", dest="type",  default="b", help="Box or Cylinder")
p.add_option("-t", "--parts", action="store", type="str", default="0.5,0.5", dest="type", help="p1,p2: z_out = p1*z1 + p2*z2.  Ie, take p1 parts of infile1 and p2 parts of infile2.  Usually p1+p2=1.0.  Default=%default")

(opts, args) = p.parse_args()

if len(args) < 3:
   print ("check input values")
   sys.exit(0)
# tuple = args.split()
(dmin, dmax,parts) = args


# orderedList()

#These are in mm multiplied by 100
# xmin = int(10.0*100)
# xmax = int(10.5*100)
# ymin = int(0.0*100)
# ymax = int(0.5*100)
# zmin = int(2.0*100)
# zmax = int(2.5*100)

xmin = int(-12.6*100)
xmax = int(12.6*100)
ymin = int(-12.2*100)
ymax = int(12.2*100)
zmin = int(-4.0*100)
zmax = int(-0.5*100)
#if opts.type == 'b':
#    (xmin, xmax, ymin, ymax, zmin, zmax, dia, parts) = args
centerDist = float(dmin)+0.02*float(dmax)
# centerDist = float(14)+0.02*float(14)
  

randomList(parts,xmin,xmax,ymin,ymax,zmin,zmax,centerDist,dmin,dmax)
#copyInjection("initial.inj", "combined.inj")

##### 20 micron model
#scale = 1.0/7.0
#convertToMicro("44000.inj", "44000-20.inj", scale)
#shift("44000-20.inj", "44000-20-shift.inj")
#haircut("44000-20-shift.inj","haircut-xmax.inj",(5.0-0.01)*1e-3)
#haircut("haircut-xmax.inj","haircut-zmin.inj",(-0.5+0.010)*1e-3)
#haircut("haircut-zmin.inj","haircut-ymax.inj",(0.1-0.010)*1e-3)
#haircut("haircut-ymax.inj","haircut-final.inj",(-0.1+0.010)*1e-3)

##### 140 micron shift
# shift("22000.inj", "22000-shift.inj")
#shift("44000.inj", "44000-140-shift.inj")
print ("DONE")
sys.exit(3)
