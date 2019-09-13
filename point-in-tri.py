import numpy as np

def calArea(p, n1, n2, n3):
    n1n2 = n2 - n1
    n1n3 = n3 - n1

    pn1 = n1 - p
    pn2 = n2 - p
    pn3 = n3 - p

    totA = np.cross(n1n2,n1n3)
    a1 = np.cross(pn1, pn2)
    a1 = np.linalg.norm(a1)
    a2 = np.cross(pn2, pn3)
    a2 = np.linalg.norm(a2)
    a3 = np.cross(pn3, pn1)
    a3 = np.linalg.norm(a3)

    print("Total area ",np.linalg.norm(totA))
    print("a1 + a2 + a3 ",a1+a2+a2)

def side(n1, n2, p):
    # return (n2[1] - n1[1])*(p[0] - n1[0]) + (-n2[0] + n1[0])*(p[1] - n1[1])
    v = np.array([(n2[1] - n1[1]),(-n2[0] + n1[0]), (n1[2] - n2[2])])
    vdash = np.array([(p[0] - n1[0]),(p[1] - n1[1]), (n1[2] - p[2])])

    return np.dot(v,vdash)

def pointInTriangle(n1, n2, n3, p):
    checkSide1 = side(n1, n2, p) <= 0
    checkSide2 = side(n2, n3, p) <= 0
    checkSide3 = side(n3, n1, p) <= 0
    print("checkSide1 ",checkSide1)
    print("checkSide2 ",checkSide2)
    print("checkSide3 ",checkSide3)
    return checkSide1 and checkSide2 and checkSide3

def readFile(fname):
#     with open (fname) as file:
    file = open(fname, "r")
    for i in range(4):
        line = file.readline()
        p_line = file.readline()
        tuple = p_line.split()
        pp = np.array([float(tuple[1]),float(tuple[2]),float(tuple[3])])
        
        n1_line = file.readline()
        tuple = n1_line.split()
        nn1 = np.array([float(tuple[1]),float(tuple[2]),float(tuple[3])])
        
        n2_line = file.readline()
        tuple = n2_line.split()
        nn2 = np.array([float(tuple[1]),float(tuple[2]),float(tuple[3])])
        
        n3_line = file.readline()
        tuple = n3_line.split()
        nn3 = np.array([float(tuple[1]),float(tuple[2]),float(tuple[3])])
        
        a_line = file.readline()
        tuple = a_line.split()
        aa = np.array([float(tuple[1]),float(tuple[2]),float(tuple[3])])
        
        # calArea(pp, nn1, nn2, nn3)
        print(pointInTriangle(nn1, nn2, nn3, pp))
        
    file.close()
    print("DONE")
        
readFile("../../Documents/sim/test2/logfile10.log")
