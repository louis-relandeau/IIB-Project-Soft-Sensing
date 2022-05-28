import cv2
import numpy as np
import glob

name = 'vid5'
path = 'Generic_ur5_controller/plotting/' + name + '/'

img_array = []
for filename in glob.glob(path + '*.png'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)


out = cv2.VideoWriter(path + name + '.avi',cv2.VideoWriter_fourcc(*'DIVX'), 5, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()