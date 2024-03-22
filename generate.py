import numpy as np
import math
import random
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

def genRandPoints(x,y,margin,numPoints=20):
    x_lims = (margin,x-margin)
    y_lims = (margin,y-margin)
    
    x_points = np.random.uniform(x_lims[0],x_lims[1],size=(1,numPoints))
    y_points = np.random.uniform(y_lims[0],y_lims[1],size=(1,numPoints))
    
    points = np.vstack((x_points,y_points)).T
    

    return points

def squaredDistance(p1,p2):
    return (p1[0]-p2[0])**2+(p1[1]-p2[1])**2

def euclideanDistance(p1,p2):
    return math.sqrt(squaredDistance(p1,p2))

def pushApart(points,distance=15):
    sq_dist = distance**2
    for i in range(points.shape[0]):
        for j in range(i+1,points.shape[0]):
            if squaredDistance(points[i],points[j]) < sq_dist and squaredDistance(points[i],points[j]) != 0.0:
                hx = points[j][0]-points[i][0]
                hy = points[j][1]-points[i][1]
                h1 = euclideanDistance(points[i],points[j])
                hx /= h1
                hy /= h1
                diff = distance-h1
                hx *= diff
                hy *=distance
                points[j][0]+= hx
                points[j][1]+= hy
                points[i][0]-= hx
                points[i][1]-= hy
                

def pushApartN(points,distance=15,itr=3):
    for _ in range(itr):
        pushApart(points,distance)
        
    return points

def getLength(points):
    dist = 0
    for i in range(1,len(points)):
        dist += euclideanDistance(points[i],points[i-1])
        
    return dist

def getHull(points):
    ch = ConvexHull(points)
    ch_p = points[ch.vertices]
    ch_p = np.vstack((ch_p,ch_p[0]))
    return ch_p

def midDisplace(points,difficulty=1.0,maxDisplacement=20.0):
    new_points = np.zeros((points.shape[0]*2,points.shape[1]))

 
    for i in range(len(points)):  
        dispLen = (random.uniform(0,1)**difficulty) * maxDisplacement;  
        disp = [0,1]
        rand_angle = random.uniform(-1,1)*math.pi
        rot_mat = np.array([[np.cos(rand_angle),np.sin(rand_angle)],[-np.sin(rand_angle),np.cos(rand_angle)]])
        disp = np.dot(disp,rot_mat)
        disp*= dispLen;  
        new_points[i*2] = points[i];  
        midpoint = points[i]+points[(i+1)%len(points)]
        midpoint /= 2
        new_points[i*2 + 1] = midpoint + disp
        

    return new_points

p = genRandPoints(300,300,10,20)

ch_p1 = getHull(p)


ch_p2 = midDisplace(ch_p1,difficulty=1,maxDisplacement=10)
ch_p2 = pushApartN(ch_p2,itr=3)
print(ch_p2)


plt.scatter(p[:,0],p[:,1],color='green')
plt.plot(ch_p1[:,0],ch_p1[:,1],color='orange')
plt.scatter(ch_p1[:,0],ch_p1[:,1],color='orange')
plt.plot(ch_p2[:,0],ch_p2[:,1],color='red')
plt.scatter(ch_p2[:,0],ch_p2[:,1],color='red')
plt.show()
