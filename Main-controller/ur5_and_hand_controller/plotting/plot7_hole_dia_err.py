from matplotlib import pyplot as plt
import numpy as np
import math

# [angle, real, measured]
diameters = np.array([[45, 5.53, 5.5],[45, 5.53, 6],[45, 5.53, 5],[47.5, 5.78, 5.5],[50, 6.06, 5.5],[52.5, 6.39, 6],[55, 6.76, 7],[60, 7.7, 8],[60, 7.7, 8],[60, 7.7, 8.5],[62.5, 8.31, 6.5],[62.5, 8.31, 6.5],[62.5, 8.31, 7.5],[62.5, 8.31, 7.5],[62.5, 8.31, 5],[62.5, 8.31, 8.5],[65, 9.03, 9],[65, 9.03, 8],[65, 9.03, 9],[67.5, 9.92, 9],[67.5, 9.92, 9],[67.5, 9.92, 8.5],[67.5, 9.92, 10],[67.5, 9.92, 9.5],[67.5, 9.92, 9.5],[70, 11.02, 10],[70, 11.02, 10],[70, 11.02, 10.5],[45,5.53,5.5],[45,5.53,6],[45,5.53,5],[47.5,5.78,5.5],[50,6.06,5.5],[52.5,6.39,6],[55,6.76,7],[75, 0, 12.5],[75, 0, 13],[42.5, 0, 4],[42.5, 0, 4.5]])


def f(x):
    return math.sqrt(l**2 + (l*math.cos(x)/math.cos(x-p))**2 - (2*l*l*math.cos(x)*math.cos(p))/math.cos(x-p))

xs = np.linspace(0,75*math.pi/180,num=1000)
d=4
l=180
p=math.atan(d/l)
# print(p*180/math.pi)
func = np.array([f(x) for x in xs]) 

error = [abs(d[2]-f(d[0]*math.pi/180)) for d in diameters]
error_perc = [abs(d[2]-f(d[0]*math.pi/180))/f(d[0]*math.pi/180)*100 for d in diameters]

# print(error)
# print(error_perc)

print("mean error = {}".format(np.mean(error_perc)))
print("std error = {}".format(np.std(error_perc)))

e1 = [(d[2]-f(d[0]*math.pi/180)) for d in diameters]
e2 = [(d[2]-f(d[0]*math.pi/180))/f(d[0]*math.pi/180)*100 for d in diameters]
plt.figure()
plt.hist(e2)

plt.figure()
plt.plot(xs*180/math.pi,func,label='theoretical')
# plt.scatter(diameters[:,0],diameters[:,1],color='black')
plt.scatter(diameters[:,0],diameters[:,2],color='red', label='experimental')
plt.xlabel("Angle of choptick to vertical (°)", fontsize=15)
plt.ylabel("Minimum diameter detectable (mm)", fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
plt.legend(loc='upper left', fontsize=15)
plt.tight_layout()
plt.show()
