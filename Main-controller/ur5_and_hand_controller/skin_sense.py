from os import name
from re import X
import time
from tkinter import Y
from cv2 import FONT_HERSHEY_DUPLEX
import numpy as np
#import nidaqmx
import _thread
import copy
from pandas import array
import scipy.optimize as optimize
import csv
import cv2
import json
import math
import random
from pathlib import Path
from scipy import signal


import kg_robot as kgr

thread_flag = False
tm_thread_flag = False
ft_thread_flag = False
pos_thread_flag = False
skin_thread_flag = False
cam_thread_flag = False
timer_flag = 0

pinching = 0
table_contact = False
found_hole = False

ft_data = []
pos_data = []
skin_data = []

filename = 'video.avi'
frames_per_second = 24.0
res = '720p'

class skin_sense():
    def __init__(self,robot):
        self.robot = robot

    def record(self,name='test',ft=True,pos=True,skin=True,cam=True):
        start_time = int(time.time())
        read_traj(self.robot,name,start_time,ft,pos,skin,cam)
        return '{}_{}_traj.json'.format(name,start_time)

    def play(self, name, ft=False, pos=False, skin=True, cam=True, rp=0):
        play_and_read(self.robot, name, ft, pos, skin, cam, rp)
        return

def test(burt):
    global thread_flag
    _thread.start_new_thread(read_data,(burt,'down-up-close-pos',0,False,True,True,False))
    time.sleep(1)
    burt.open_gripper()
    time.sleep(2)
    burt.movel([-0.1259,-0.3339,0.1672,0.0937,2.753,-1.263])
    time.sleep(1)
    burt.close_gripper()
    time.sleep(2)
    burt.home()
    burt.open_gripper()
    time.sleep(1)
    thread_flag = False

def take_pic(name):
    cap = cv2.VideoCapture(1,cv2.CAP_DSHOW )
    cap.set(cv2.CAP_PROP_AUTOFOCUS,0)
    ret, frame = cap.read()
    t = time.ctime().replace('  ','-').replace(' ','-').replace(':','.')
    pic_name = name + '/' + t + '_data'
    cv2.imwrite('Generic_ur5_controller/data/{}.jpg'.format(pic_name), frame)
    print('taking picture')
    cap.release()

def pick_up(burt, name='test'):
    global thread_flag
    global pinching
    print('starting recording')
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,True))
    time.sleep(3)
    burt.home(wait = False)
    time.sleep(3)
    N=1000
    down = 0.02786 
    for _ in range(N):
        offset = random.uniform(-0.005, 0.005)
        xy = (down + offset) * 2**(-0.5)
        # burt.movel_tool([xy,xy,0,0,0,0], acc=0.1, vel=0.03, wait = False)
        # time.sleep(2)
        burt.close_gripper()
        time.sleep(2)
        pinching = 1
        # burt.movel_tool([-xy,-xy,0,0,0,0], acc=0.1, vel=0.03, wait = False)
        # time.sleep(2)
        pinching = 0
        burt.open_gripper()
        time.sleep(2)

    burt.home(wait = False)
    print('ending recording')
    thread_flag = False

def chopstick1(burt,angle,name='test'): 
    global thread_flag
    pos_above = [-0.1036,-0.3780,0.3170,0.0384,-2.762,1.515]
    pos_chop = [-0.1036,-0.3780,0.2570,0.0384,-2.762,1.515]
    translation = [-0.1036 + (0.01*math.cos(angle*2*math.pi/360)),-0.3780 + (0.01*math.sin(angle*2*math.pi/360)),0.2570,0.0384,-2.762,1.515]
    burt.movel(pos_above)
    time.sleep(0.5)
    burt.movel(pos_chop)
    time.sleep(1)
    burt.close_gripper()
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,False))
    time.sleep(2.5)
    burt.movel(translation)
    time.sleep(1)
    burt.movel(pos_chop)
    time.sleep(0.5)
    burt.open_gripper()
    time.sleep(1)
    burt.movel(pos_above)
    thread_flag = False

def chopstick2(burt, name='test'): # this is angle change using cone
    global thread_flag
    start_pos_above = [-0.1173,-0.48,0.2518,0.6877,1.794,-1.8667]
    start_pos = [-0.1173,-0.48,0.165,0.6877,1.794,-1.8667]
    cone_pos_above = [-0.1879,-0.5339,0.2518,0.974,1.794,-2.042]
    cone_pos = [-0.1879,-0.5339,0.206,0.974,1.794,-2.042]
    print('starting recording')
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,False))
    time.sleep(3)
    burt.movel(start_pos_above, wait = False)
    burt.movel(start_pos, wait=False)
    time.sleep(3)
    burt.close_gripper()
    time.sleep(2)
    burt.movel(start_pos_above, wait = False)
    time.sleep(2)
    burt.movel(cone_pos_above, wait=False)
    time.sleep(2)
    burt.movel(cone_pos, wait=False)
    time.sleep(2)
    N=5
    for _ in range(N):
        angle = random.uniform(0, 360)
        translation = list(np.array(cone_pos) + np.array([0.05*math.cos(angle*2*math.pi/360),0.05*math.sin(angle*2*math.pi/360),-0.01,0,0,0]))
        burt.movel(translation, wait=False)
        # time.sleep(3)
        burt.movel(cone_pos, wait=False)
        time.sleep(2)

    burt.movel(cone_pos_above, wait=False)
    time.sleep(3)
    burt.movel(start_pos_above, wait = False)
    time.sleep(3)
    burt.open_gripper()
    time.sleep(3)
    # time.sleep(N*16) # to move to max angle and back, this loop takes approximately 16s but there is an interrup in read_data is static for too long (doesn't exit fcn though)
    print('ending recording')
    thread_flag = False

def chopstick3(burt, name='test'): # this is angle change with chopstick stuck in table
    global thread_flag
    start_pos_above = [-0.1173,-0.48,0.2518,0.6877,1.794,-1.8667]
    start_pos = [-0.1173,-0.48,0.165,0.6877,1.794,-1.8667]
    print('starting recording')
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,False))
    time.sleep(3)
    burt.movel(start_pos_above, wait = False)
    time.sleep(3)
        
    N=5
    for _ in range(N):
        burt.movel(start_pos, wait=False)
        time.sleep(3)
        burt.close_gripper()
        time.sleep(3)
        angle = random.uniform(0, 360)
        translation = list(np.array(start_pos) + np.array([0.01*math.cos(angle*2*math.pi/360),0.01*math.sin(angle*2*math.pi/360),0,0,0,0]))
        burt.movel(translation, wait=False)
        # time.sleep(3)
        burt.open_gripper()
        time.sleep(2)

    burt.movel(start_pos, wait=False)
    time.sleep(3)
    burt.movel(start_pos_above, wait=False)
    time.sleep(3)
    # time.sleep(N*16) # to move to max angle and back, this loop takes approximately 16s but there is an interrup in read_data is static for too long (doesn't exit fcn though)
    print('ending recording')
    thread_flag = False

def chopstick4(burt, name='test'): # this is angle change with chopstick stuck in ball joint
    global thread_flag
    N = 200 # repeat 200 times 
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW ) # start camera, set to 1 if it isn't default laptop camera
    cap.set(cv2.CAP_PROP_AUTOFOCUS,0)
    for i in range(N):
        burt.stream_data_start(0.01)
        time.sleep(1)
        burt.stream_data_stop(wait=False)
        time.sleep(1)
        if i <= 1: # skipping the first two recordings because data wasn't recorded properly
            print('skipping {}'.format(i)) 
            _thread.start_new_thread(read_data,(burt,name,0,False,True,True,False)) # no video
            time.sleep(3)  
            thread_flag = False

        else:
            burt.home(wait=False)
            time.sleep(3)
            print('starting recording ({}/{})'.format(i+1,N))
            _thread.start_new_thread(read_data,(burt,name,0,False,True,True,False))
            time.sleep(3)
            burt.close_gripper() # close around gripper
            time.sleep(3)  
            burt.movel_tool([-0.05,-0.05,0.045,0,0,0], acc=0.1, vel=0.03, wait = False) # move above ball joint
            time.sleep(4)  
            l = 0.025
            for j in range(10): # move around the vertical of the ball joint 10 times 
                z = random.uniform(-l, l)
                xy = random.uniform(-l, l) * 2**(-0.5)
                burt.movel_tool([xy,xy,z,0,0,0], acc=0.1, vel=0.03, wait = False)
                time.sleep(2)
                burt.movel_tool([-xy,-xy,-z,0,0,0], acc=0.1, vel=0.03, wait = False)
                time.sleep(2)
                ret, frame = cap.read()
                if j == 5: # take a picture in the middle to check chopstick hasn't been lost                
                    t = time.ctime().replace('  ','-').replace(' ','-').replace(':','.')
                    pic_name = name + '/' + t + '_data'
                    cv2.imwrite('Generic_ur5_controller/data/{}.jpg'.format(pic_name), frame)
                    print('taking picture')
            burt.movel_tool([0.05,0.05,-0.045,0,0,0], acc=0.1, vel=0.03, wait = False) # return home
            time.sleep(4) 
            burt.open_gripper() # release chopstick
            
            time.sleep(3)  

            print('ending recording ({}/{})'.format(i+1,N))
            
            thread_flag = False
    cap.release()

def chopstick5(burt, name='test'): # this is angle change (+hand angle) with chopstick stuck in ball joint
    global thread_flag
    global pos_data
    N = 100
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW )
    cap.set(cv2.CAP_PROP_AUTOFOCUS,0)
    for i in range(N):
        burt.stream_data_start(0.01)
        time.sleep(1)
        burt.stream_data_stop(wait=False)
        time.sleep(1)
        # if i <= 1:
        #     print('skipping {}'.format(i))
        #     _thread.start_new_thread(read_data,(burt,name,0,False,True,True,False))
        #     time.sleep(3)  
        #     thread_flag = False

        # else:
        burt.home(wait=False)
        time.sleep(3)
        print('starting recording ({}/{})'.format(i+1,N))
        _thread.start_new_thread(read_data,(burt,name,0,False,True,True,False))
        time.sleep(3)
        
        hand_angle = random.uniform(-30,30) * math.pi / 180
        burt.movel_tool([0,0,0,0,0,hand_angle], acc=0.1, vel=0.03, wait = False)
        time.sleep(5)
        if pos_data != [0, 0, 0, 0, 0, 0]:
            pose = pos_data.copy()
        print('pose: ', pose)

        burt.close_gripper()
        time.sleep(3)  

        x = -0.02
        y = -0.075
        z = 0.01
        
        pose[0]+=x
        pose[1]+=y
        pose[2]+=z
        burt.movel(pose, acc=0.1, vel=0.03, wait = False)
        # burt.translatel_rel([-0.05,-0,0,0,0,0], acc=0.1, vel=0.03, wait = False)
        time.sleep(3)  
        
        l = 0.025
        for j in range(10):
            x1 = random.uniform(-l, l)
            y1 = random.uniform(-l, l)
            pose[0]+=x1
            pose[1]+=y1
            burt.movel(pose, acc=0.1, vel=0.03, wait = False)
            time.sleep(2)
            pose[0]-=x1
            pose[1]-=y1
            burt.movel(pose, acc=0.1, vel=0.03, wait = False)
            time.sleep(2)

            ret, frame = cap.read()
            if j == 8:                    
                t = time.ctime().replace('  ','-').replace(' ','-').replace(':','.')
                pic_name = name + '/' + t + '_data'
                time.sleep(0.5)
                cv2.imwrite('Generic_ur5_controller/data/{}.jpg'.format(pic_name), frame)
                print('taking picture')

        
        pose[0]-=x
        pose[1]-=y
        pose[2]-=z
        burt.movel(pose, acc=0.1, vel=0.03, wait = False)
        time.sleep(4) 
        burt.open_gripper()
        
        time.sleep(3)  
        burt.movel_tool([0,0,0,0,0,-hand_angle], acc=0.1, vel=0.03, wait = False)
        print('ending recording ({}/{})'.format(i+1,N))
        
        thread_flag = False
    cap.release()

def chopstick6(burt, name='test'): # angle line experiment 4 sensors
    global thread_flag
    global pos_data
    N = 100
    L = 0.16
    points = 10 # one more than step
    total_angle = 45
    degrees = total_angle / points
    ys = []
    zs = []
    diffy = []
    diffz = []
    for i in range(points): # the angle thing doesn't work yet
        ys.append(L * math.sin(i*degrees*math.pi/180))
        zs.append(L * (1-math.cos(i*degrees*math.pi/180)))
    for i in range(points-1):
        diffy.append(ys[i+1]-ys[i])
        diffz.append(zs[i+1]-zs[i])
    print(ys, diffy)
    # burt.open_gripper()
    burt.home(wait=False)
    time.sleep(3)
    # burt.close_gripper()
    # time.sleep(10)  
    burt.stream_data_start(0.01)
    time.sleep(1)
    burt.stream_data_stop(wait=False)
    time.sleep(1)
    print("Starting recording")
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,False))
    time.sleep(3)
    # burt.translatel_rel([0,-0.03,0,0,0,0], acc=0.1, vel=0.03, wait = False) #moves outward
    # time.sleep(3)  
    for i in range(N):
        print('{}/{}...'.format(i+1,N))
        time.sleep(5)
        # burt.translatel_rel([0,+0.06,0,0,0,0], acc=0.1, vel=0.03, wait = False)
        # time.sleep(3)  
        # burt.translatel_rel([0,-0.06,0,0,0,0], acc=0.1, vel=0.03, wait = False)
        # time.sleep(3)
        for j in range(len(diffy)):
            burt.translatel_rel([0,-diffy[j],-diffz[j],0,0,0], acc=0.1, vel=0.03, wait = False)
            # time.sleep(1)  
        for j in range(len(diffy)):
            burt.translatel_rel([0,+diffy[-(j+1)],diffz[-(j+1)],0,0,0], acc=0.1, vel=0.03, wait = False)
            # time.sleep(1)  
    # burt.translatel_rel([0,+0.03,0,0,0,0], acc=0.1, vel=0.03, wait = False)
    # time.sleep(3)  
    print("Ending recording")
    thread_flag = False
    time.sleep(3)
    # burt.open_gripper()
    # time.sleep(3)  

def contour1(burt, name='test'): # straight line gets different angles
    global thread_flag
    burt.home(wait=False)
    time.sleep(3)
    burt.stream_data_start(0.01)
    time.sleep(1)
    burt.stream_data_stop(wait=False)
    time.sleep(1)
    print("Starting recording")
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,False))
    time.sleep(3)

    burt.translatel_rel([0.25,0,0,0,0,0], acc=0.1, vel=0.01, wait = False) # -ve y outward from lab door, +ve x is towards palpation setup
    time.sleep(30)  

    print("Ending recording")
    thread_flag = False
    time.sleep(3)

def contour2(burt, name='test'): # should go up and down with surface thus recording height through position
    global thread_flag
    burt.home(wait=False)
    time.sleep(3)
    burt.stream_data_start(0.01)
    time.sleep(1)
    burt.stream_data_stop(wait=False)
    time.sleep(1)
    print("Starting recording")
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,True))
    time.sleep(3)

    global pos_data
    start_position = copy.copy(pos_data)

    dist = 0.25 # distance to cover in x
    steps = 0.001 # distance between two points in x
    v = 0.005 # travelling speed in x
    n = int((dist//steps)+1) # number of steps in x

    l = 3*steps # distance to move in z
    sum_l = 0 # incremented z pos
    # print(n)
    seq_pos = np.linspace(0, dist, num=n) 
    seq_t = np.ones_like(seq_pos) * steps/v

    data_arr = []
    t = 4*seq_t[0]
    global skin_data
    data_arr.append(copy.copy(skin_data))
    time.sleep(2*t)
    burt.servoj(np.array([0,0,-4*l,0,0,0])+start_position,control_time=t,lookahead_time=0.008,gain=300)
    time.sleep(4*t)
    data_arr.append(copy.copy(skin_data))
    time.sleep(2*t)
    burt.servoj(np.array([0,0,4*l,0,0,0])+start_position,control_time=t,lookahead_time=0.008,gain=300)
    time.sleep(4*t)
    data_arr.append(np.array(copy.copy(skin_data)))
    time.sleep(2*t)
    burt.home()
    time.sleep(2*t)
    print(data_arr)

    i = 0
    while i < len(seq_pos):
        current_skin = np.array(copy.copy(skin_data))
        dist = np.array([0,0,0])
        for j in range(len(data_arr)):
            dist[j] = np.linalg.norm(current_skin-data_arr[j])
        min_index = np.where(dist==min(dist))[0][0]
        if min_index == 0:
            pass
        elif min_index == 1:
            sum_l += l
        elif min_index == 2:
            sum_l -= l
        print(dist, min(dist), min_index, sum_l)        

        burt.servoj(np.array([0,-seq_pos[i],sum_l,0,0,0])+start_position,control_time=seq_t[i],lookahead_time=0.008,gain=300) # +ve x is towards palpation setup, +ve y towards lab door
        time.sleep(seq_t[i]) # prevents loop to finish too fast, motion not as smooth
        i+=1
        

    print("Ending recording in 3s") # so camera can record more
    time.sleep(3)
    thread_flag = False
    time.sleep(3)

def contour3(burt, name='test'): # new profile, and proportional controller?
    global thread_flag
    burt.home(wait=False)
    time.sleep(3)
    burt.stream_data_start(0.01)
    time.sleep(1)
    burt.stream_data_stop(wait=False)
    time.sleep(1)
    print("Starting recording")
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,True))
    time.sleep(3)

    global pos_data
    start_position = copy.copy(pos_data)

    dist = 0.13 # distance to cover in y
    steps = 0.004 # distance between two points in y
    v = 0.005 # travelling speed in y
    n = int((dist//steps)+1) # number of steps in y

    l = 0.001 # distance to move in z
    sum_l = 0 # incremented z pos
    # print(n)
    seq_pos = np.linspace(0, dist, num=n) 
    seq_t = np.ones_like(seq_pos) * steps/v

    data_arr = []
    t = 2
    d = 0.005
    global skin_data
    data_arr.append(copy.copy(skin_data))
    time.sleep(t)
    burt.servoj(np.array([0,0,-d,0,0,0])+start_position,control_time=t,lookahead_time=0.008,gain=300)
    time.sleep(t)
    data_arr.append(copy.copy(skin_data))
    time.sleep(t)
    burt.servoj(np.array([0,0,d,0,0,0])+start_position,control_time=t,lookahead_time=0.008,gain=300)
    time.sleep(t)
    data_arr.append(np.array(copy.copy(skin_data)))
    time.sleep(t)
    burt.home()
    time.sleep(2*t)
    print(data_arr)

    i = 0
    while i < len(seq_pos):
        current_skin = np.array(copy.copy(skin_data))
        dist = np.array([0,0,0])
        for j in range(len(data_arr)):
            dist[j] = np.linalg.norm(current_skin-data_arr[j])
        min_index = np.where(dist==min(dist))[0][0]
        if min_index == 0:
            pass
        elif min_index == 1:
            sum_l += l
        elif min_index == 2:
            sum_l -= l
        print(dist, min(dist), min_index, sum_l)        

        burt.servoj(np.array([0,-seq_pos[i],sum_l,0,0,0])+start_position,control_time=seq_t[i],lookahead_time=0.008,gain=300) # +ve x is towards palpation setup, +ve y towards lab door
        time.sleep(seq_t[i]) # prevents loop to finish too fast, motion not as smooth
        i+=1
        

    print("Ending recording in 3s") # so camera can record more
    time.sleep(3)
    thread_flag = False
    time.sleep(3)

def freq1(burt, name='test'): # freq sweep
    global thread_flag
    burt.home(wait=False)
    time.sleep(3)
    burt.stream_data_start(0.01)
    time.sleep(1)
    burt.stream_data_stop(wait=False)
    time.sleep(1)
    print("Starting recording")
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,False))
    time.sleep(3)

    global pos_data
    start_position = np.array(copy.copy(pos_data))

    # mag = 0.05
    # speeds = np.linspace(0.02, 0.1, num=100)
    # # speeds = np.ones_like(speeds) * 0.02
    # for s in speeds:
    #     burt.translatel_rel([mag,0,0,0,0,0], acc=0.1, vel=s, wait = False) # +ve y outward from lab door, +ve x is towards palpation setup
    #     burt.translatel_rel([-mag,0,0,0,0,0], acc=0.1, vel=s, wait = False)
    # time.sleep(30)  

    time_step = .01
    time_vec = np.arange(0, 30, time_step)
    sig = np.sin(0.5 * np.pi * time_vec * (1 + .1 * time_vec))
    for s in sig:
        burt.servoj(np.array([0,s*0.01,0,0,0,0])+start_position,control_time=time_step,lookahead_time=0.008,gain=300) # +ve x is towards palpation setup, +ve y towards lab door
        time.sleep(time_step)

    print("Ending recording")
    time.sleep(3)
    thread_flag = False
    time.sleep(3)

def speed1(burt, name='test'): # fast response, increasing speed, see when it looses it
    global thread_flag
    # burt.home(wait=False)
    time.sleep(3)
    burt.stream_data_start(0.01)
    time.sleep(1)
    burt.stream_data_stop(wait=False)
    time.sleep(1)
    print("Starting recording")
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,False))
    time.sleep(3)

    global pos_data
    start_position = np.array(copy.copy(pos_data))

    mag = 0.01
    speeds = np.linspace(0.01, 1, num=10)
    print(speeds)
    for s in speeds:
        burt.movel(np.array([0,0,mag,0,0,0])+start_position, acc=5, vel=s, wait = False) # +ve y outward from lab door, +ve x is towards palpation setup
        burt.movel(np.array([0,0,-mag,0,0,0])+start_position, acc=5, vel=s, wait = False)
        time.sleep(3)  

    print("Ending recording")
    time.sleep(3)
    thread_flag = False
    time.sleep(3)

def find_hole1(burt, name='test'): # stops at a hole in the table while dragging chocpstick
    global thread_flag
    global pos_data
    burt.home(wait=False)
    time.sleep(3)
    burt.stream_data_start(0.01)
    time.sleep(1)
    burt.stream_data_stop(wait=False)
    time.sleep(1)
    print("Starting recording")
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,True))
    time.sleep(5)

    # start_position = np.array(burt.getl())
    start_position = copy.copy(pos_data)
    # initial_data = np.array(copy.copy(skin_data))

    dist = 0.10
    steps = 0.002
    v = 0.02
    n = int((dist//steps)+1)
    l = 0.005 # distance between two sweeping lines
    sum_l = 0 # incremented lines
    # print(n)
    seq_pos = np.linspace(0, dist, num=n) 
    seq_t = np.ones_like(seq_pos) * steps/v
    # print(seq_pos)
    # print(seq_t)

    i = 0
    global found_hole
    # while found_hole == False and i < len(seq_pos):
    #     # print('Moving...')
    #     burt.servoj(np.array([seq_pos[i],0,0,0,0,0])+start_position,control_time=seq_t[i],lookahead_time=0.008,gain=300) 
    #     i+=1
    #     time.sleep(dist/v/(dist//steps)) # prevents loop to finish too fast, is motion still smooth?
    
    while found_hole == False:
        i = 0
        while found_hole == False and i < len(seq_pos):
            burt.servoj(np.array([seq_pos[i],sum_l,0,0,0,0])+start_position,control_time=seq_t[i],lookahead_time=0.008,gain=300) # +ve x is towards palpation setup, +ve y towards lab door
            time.sleep(seq_t[i]) # prevents loop to finish too fast, motion not as smooth
            i+=1
        if i == len(seq_pos):   
            print('not on previous line')
            sum_l += l
            burt.servoj(np.array([0,sum_l,0,0,0,0])+start_position,control_time=(dist+l)/v/4,lookahead_time=0.008,gain=300)
            time.sleep((dist+l)/v/4)

    time.sleep(1)
    burt.translatel_rel([0,0,-0.03,0,0,0], acc=0.1, vel=0.01, wait = False)
    print("Ending recording in 3s") # so camera can record more
    time.sleep(3)
    thread_flag = False
    time.sleep(3)

def hole2(burt, name='test'): # straight line gets different angles
    global thread_flag
    burt.home(wait=False)
    time.sleep(3)
    burt.stream_data_start(0.01)
    time.sleep(1)
    burt.stream_data_stop(wait=False)
    time.sleep(1)
    print("Starting recording")
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,True))
    time.sleep(3)

    burt.translatel_rel([0,-0.28,0,0,0,0], acc=0.1, vel=0.01, wait = False) # -ve y outward from lab door, +ve x is towards palpation setup
    time.sleep(33)  

    print("Ending recording")
    thread_flag = False
    time.sleep(3)

def rep(burt, name='test'): # repeating contact with flat surface
    global thread_flag
    N = 1000
    move_out = [-2.75362, -2.05813, -2.03456, 0.277342, 1.09408, 0.981765]
    move_in = [-2.73639, -2.02589, -2.09226, 0.298902, 1.08252, 0.993999]
    burt.movej(move_out, acc=0.1, vel=0.05, wait = False) 
    time.sleep(5)  

    burt.stream_data_start(0.01)
    time.sleep(1)
    burt.stream_data_stop(wait=False)
    time.sleep(1)
    print("Starting recording")
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,False))
    time.sleep(3)

    for i in range(N):
        print('Step {}/{}...'.format(i,N))
        burt.movej(move_in, acc=0.1, vel=0.05, wait = False) 
        time.sleep(2)
        burt.movej(move_out, acc=0.1, vel=0.05, wait = False) 
        time.sleep(2)  

    print("Ending recording")
    thread_flag = False
    time.sleep(3)

    
def tau1(burt, name='test'): # observing time response of one sensor, very fast move out
    global thread_flag
    move_out = [-2.74043, -2.0337, -2.07816, 0.29392, 1.0855, 0.991037]
    move_in = [-2.73369, -2.02086, -2.10141, 0.302143, 1.08047, 0.995942]
    burt.home(wait=False)
    time.sleep(5)

    burt.stream_data_start(0.01)
    time.sleep(1)
    burt.stream_data_stop(wait=False)
    time.sleep(1)
    print("Starting recording")
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,False))
    time.sleep(3)

    burt.movej(move_out, acc=10, vel=5, wait = False) 
    time.sleep(5)  

    print("Ending recording")
    thread_flag = False
    time.sleep(3)

def tau2(burt, name='test'): # observing time response of one sensor, leaking
    global thread_flag
    move_out = [-2.75362, -2.05813, -2.03456, 0.277342, 1.09408, 0.981765]
    move_in = [-2.73639, -2.02589, -2.09226, 0.298902, 1.08252, 0.993999]
    total = 600
    # burt.home(wait=False)
    # time.sleep(5)
    burt.movej(move_out, acc=1, vel=0.1, wait = False) 
    time.sleep(10)  

    burt.stream_data_start(0.01)
    time.sleep(1)
    burt.stream_data_stop(wait=False)
    time.sleep(1)
    print("Starting recording")
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,False))
    time.sleep(total/2)

    burt.movej(move_in, acc=1, vel=0.1, wait = False) 
    time.sleep(total)  
    burt.movej(move_out, acc=1, vel=0.1, wait = False) 
    time.sleep(total)  

    print("Ending recording")
    thread_flag = False
    time.sleep(3)

def simple_record(burt, name='test'): # no move, just record
    global thread_flag
    move_out = [-2.75362, -2.05813, -2.03456, 0.277342, 1.09408, 0.981765]
    burt.movej(move_out, acc=1, vel=0.1, wait = False) 
    time.sleep(10)  

    burt.stream_data_start(0.01)
    time.sleep(1)
    burt.stream_data_stop(wait=False)
    time.sleep(1)
    print("Starting recording")
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,False))

    for _ in range(10):
        time.sleep(8)
        print('press')
        time.sleep(2)
        print('release')

    print("Ending recording")
    thread_flag = False
    time.sleep(3)

def min_angle1(burt, name='test'): # decrease angle moved by until can't read
    global thread_flag
    # burt.home(wait=False)
    time.sleep(3)
    burt.stream_data_start(0.01)
    time.sleep(1)
    burt.stream_data_stop(wait=False)
    time.sleep(1)
    print("Starting recording")
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,False))
    time.sleep(3)

    global pos_data
    start_position = np.array(copy.copy(pos_data))

    # dist = np.linspace(0.02, 0.0002, num=50)
    dist = np.linspace(0.0002, 0.02, num=50)
    print(dist)
    for d in dist:
        burt.movel(np.array([0,-d,0,0,0,0])+start_position, acc=0.1, vel=0.02, wait = False) # +ve y towards door
        time.sleep(5)
        burt.movel(start_position, acc=5, vel=0.02, wait = False)
        time.sleep(5)  

    print("Ending recording")
    time.sleep(3)
    thread_flag = False
    time.sleep(3)

def table1(burt,angles,name='test'):
    global thread_flag
    #burt.ee_start_streaming()
    base = [-0.140,-0.534,0.374,0.49,1.082,-2.254]
    burt.movel(base, wait = False)
    time.sleep(0.5)
    _thread.start_new_thread(read_data,(burt,name,0,False,False,True,False))
    time.sleep(2)
    burt.movel([-0.140,-0.534,0.31,0.49,1.082,-2.254],wait = False)
    burt.movel_tool([0,0,0,0,0,angles[2]], acc=0.1, vel=0.1, wait = False)
    burt.movel_tool([0,0,0,angles[0],angles[1],0], acc=0.1, vel=0.1, wait = False)
    time.sleep(5)
    burt.movel(base, wait = False)
    time.sleep(1)
    #burt.ee_stop_streaming()
    thread_flag = False

def table2(burt,name='test'):
    global thread_flag
    print('Starting recording')
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,False))
    time.sleep(3)
    burt.home()
    N=450
    for i in range(N):
        print('Move {}/{}...'.format(i,N))
        # a1 = np.array([0,0,1])
        # a2 = np.array([1/math.sqrt(2),-1/math.sqrt(2),0])
        # r1 = a1 * (random.uniform(-15, 15) * math.pi /180)
        # r2 = a2 * (random.uniform(-15, 15) * math.pi /180)

        r = np.array([random.uniform(-15, 15),random.uniform(-15, 15),random.uniform(-15, 15)]) * math.pi / 180 
        burt.movel_tool([0,0,0,r[0],r[1],r[2]], acc=0.1, vel=0.03, wait = False)
        burt.home()
        time.sleep(5)
    
    
    print('Stopping recording')
    thread_flag = False

def table3(burt,name='test'): # this is demo for camera sync
    global thread_flag
    base = [-0.140,-0.534,0.300,0.49,1.082,-2.254]
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,True))
    time.sleep(3)
    burt.movel(base, wait = False)
    for _ in range(3):
        burt.home(wait = False)
        burt.movel(base, wait = False)
    N=1
    for i in range(N):
        print('Move {}/{}...'.format(i,N))
        a1 = np.array([0,0,1])
        a2 = np.array([1/math.sqrt(2),-1/math.sqrt(2),0])
        r1 = a1 * -15 * math.pi /180
        r2 = a2 * 15 * math.pi /180
        burt.movel_tool([0,0,0,0,0,r1[2]], acc=0.1, vel=0.015, wait = False)
        burt.movel_tool([0,0,0,r2[0],r2[1],0], acc=0.1, vel=0.015, wait = False)
        burt.movel(base, acc=0.1, vel=0.015, wait = False)
    burt.home(wait = False)
    time.sleep(N*16) # to move to max angle and back, this loop takes approximately 16s but there is an interrup in read_data is static for too long (doesn't exit fcn though)
    thread_flag = False


def demo_IROS(burt, name='test'): # observing time response of one sensor, leaking
    global thread_flag
    global pos_data
    global table_contact
    table_contact=False
    # start = [-1.3248, -1.55758, -2.33911, 4.05787, -0.12072, -1.61091]
    # pick1 = [-1.37041, -1.68728, -2.19713, 4.00304, -0.165701, -1.56829]
    # pick2 = [-1.3923, -1.6918, -2.19136, 3.98807, -0.187527, -1.55453]
    begin = [-1.30718, -1.78234, -2.58127, 5.72109, -0.354607, -2.91942]
    grip = [-1.36545, -1.8053, -2.45608, 5.47346, -0.372286, -2.76419]
    lift = [-1.39487, -1.4542, -2.27324, 4.88633, -0.386909, -2.70696]
    above = [-1.81404, -1.3989, -2.26657, 4.25447, -0.669608, -2.06408]
    down = [-1.78765, -1.516, -2.47276, 4.46139, -0.598473, -1.96479]
    rotate = [-1.79787, -1.47685, -2.19652, 3.48873, -0.549288, -1.28877]
    burt.movej(begin, acc=1, vel=0.3, wait = False) 
    burt.open_gripper()
    time.sleep(5)  

    burt.stream_data_start(0.01)
    time.sleep(1)
    burt.stream_data_stop(wait=False)
    time.sleep(1)
    print("Starting recording")
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,True,True))
    time.sleep(5)

    burt.movej(grip, acc=1, vel=0.2, wait = False) 
    time.sleep(2)
    burt.close_gripper()
    time.sleep(2)
    burt.movej(lift, acc=0.1, vel=0.2, wait = False)
    time.sleep(3)
    burt.movej(above, acc=0.1, vel=0.2, wait = False)
    time.sleep(10)
    burt.movej(down, acc=0.1, vel=0.1, wait = False)
    time.sleep(5)
    burt.movej(rotate, acc=0.1, vel=0.1, wait = False)
    time.sleep(20)

    ##########################################################

    # start_position = np.array(burt.getl())
    start_position = copy.copy(pos_data)
    # initial_data = np.array(copy.copy(skin_data))

    dist = 0.1
    steps = 0.002
    v = 0.02
    n = int((dist//steps)+1)
    l = 0.005 # distance between two sweeping lines
    sum_l = 0 # incremented lines
    # print(n)
    seq_pos = np.linspace(0, dist, num=n) 
    seq_t = np.ones_like(seq_pos) * steps/v
    # print(seq_pos)
    # print(seq_t)

    i = 0
    global found_hole
    table_contact = True
    line_counter = 0
    coef = 1.05
    while found_hole == False:
        i = 0
        while found_hole == False and i < len(seq_pos):
            table_contact = True
            burt.servoj(np.array([seq_pos[i],sum_l,0,0,0,0])+start_position,control_time=coef*seq_t[i],lookahead_time=0.008,gain=300) # +ve x is towards palpation setup, +ve y towards lab door
            time.sleep(seq_t[i]) # prevents loop to finish too fast, motion not as smooth
            i+=1
        if i == len(seq_pos):
            table_contact = False
            print('Not on previous line ({})'.format(line_counter))   
            line_counter += 1
            sum_l += l
            burt.servoj(np.array([0,sum_l,0,0,0,0])+start_position,control_time=(dist+l)/v/1.5,lookahead_time=0.008,gain=300)
            time.sleep((dist+l)/v/1.5)
        if sum_l >= 0.05:
            print('Reached limit of lines')
            found_hole = True    

    ##########################################################

    print('Detected sensor variation')
    time.sleep(3)
    burt.translatel_rel([-0.07,0,0,0,0,0], acc=0.1, vel=0.1, wait = False) # move above hole 
    time.sleep(3)
    burt.open_gripper()
    time.sleep(3)
    ##########################################################

    print("Ending recording")
    thread_flag = False
    time.sleep(3)

def demo_IROS_hole(burt, name='test'): # observing time response of one sensor, leaking
    global thread_flag
    global pos_data
    global table_contact
    table_contact=False
    burt.home()
    begin = [-1.30718, -1.78234, -2.58127, 5.72109, -0.354607, -2.91942]
    grip = [-1.36545, -1.8053, -2.45608, 5.47346, -0.372286, -2.76419]
    lift = [-1.39487, -1.4542, -2.27324, 4.88633, -0.386909, -2.70696]
    above = [-1.81404, -1.3989, -2.26657, 4.25447, -0.669608, -2.06408]
    down = [-1.78765, -1.516, -2.47276, 4.46139, -0.598473, -1.96479]
    # rotate = [-1.79787, -1.47685, -2.19652, 3.48873, -0.549288, -1.28877]
    # burt.movej(begin, acc=1, vel=0.3, wait = False) 
    # burt.open_gripper()
    # time.sleep(5)  

    burt.stream_data_start(0.01)
    time.sleep(1)
    burt.stream_data_stop(wait=False)
    time.sleep(1)
    print("Starting recording")
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,True,True))
    time.sleep(5)

    # burt.movej(grip, acc=1, vel=0.2, wait = False) 
    # time.sleep(2)
    burt.close_gripper()
    time.sleep(15)
    # burt.movej(lift, acc=0.1, vel=0.2, wait = False)
    # time.sleep(3)
    # burt.movej(above, acc=0.1, vel=0.2, wait = False)
    # time.sleep(10)
    # burt.movej(down, acc=0.1, vel=0.1, wait = False)
    # time.sleep(5)
    # burt.movej(rotate, acc=0.1, vel=0.1, wait = False)
    # time.sleep(20)

    ##########################################################

    # start_position = np.array(burt.getl())
    start_position = copy.copy(pos_data)
    # initial_data = np.array(copy.copy(skin_data))

    dist = 0.1
    steps = 0.002
    v = 0.02
    n = int((dist//steps)+1)
    l = 0.005 # distance between two sweeping lines
    sum_l = 0 # incremented lines
    # print(n)
    seq_pos = np.linspace(0, dist, num=n) 
    seq_t = np.ones_like(seq_pos) * steps/v
    # print(seq_pos)
    # print(seq_t)

    i = 0
    global found_hole
    table_contact = True
    line_counter = 0
    coef = 1.05
    while found_hole == False:
        i = 0
        while found_hole == False and i < len(seq_pos):
            table_contact = True
            burt.servoj(np.array([seq_pos[i],sum_l,0,0,0,0])+start_position,control_time=coef*seq_t[i],lookahead_time=0.008,gain=300) # +ve x is towards palpation setup, +ve y towards lab door
            time.sleep(seq_t[i]) # prevents loop to finish too fast, motion not as smooth
            i+=1
        if i == len(seq_pos):
            table_contact = False
            print('Not on previous line ({})'.format(line_counter))   
            line_counter += 1
            sum_l += l
            burt.servoj(np.array([0,sum_l,0,0,0,0])+start_position,control_time=(dist+l)/v/1.5,lookahead_time=0.008,gain=300)
            time.sleep((dist+l)/v/1.5)
        if sum_l >= 0.05:
            print('Reached limit of lines')
            found_hole = True    

    ##########################################################

    print('Detected sensor variation')
    burt.translatel_rel([+0.08,0,0,0,0,0], acc=0.1, vel=0.1, wait = False) # move above hole 
    time.sleep(1.5)
    burt.open_gripper()
    time.sleep(2)
    burt.translatel_rel([0,0.1,0,0,0,0], acc=0.1, vel=0.1, wait = False) 
    time.sleep(10)
    ##########################################################

    print("Ending recording")
    thread_flag = False
    time.sleep(3)

def demo_IROS_pick(burt, name='test'): # observing time response of one sensor, leaking
    global thread_flag
    global pos_data
    global table_contact
    table_contact=False
    # burt.home()
    begin = [-2.39195, -1.66208, -2.11127, 3.87973, -1.39399, -1.42244]
    grip = [-2.29499, -1.75316, -2.05574, 3.91854, -1.29781, -1.43284]
    lift = [-2.17934, -1.69827, -1.69919, 3.51395, -1.17825, -1.4499]
    above = [-1.62448, -1.35729, -2.02728, 3.57592, -0.629143, -1.55586]
    down = [-1.62325, -1.48391, -2.23634, 3.90817, -0.631705, -1.55164]
    burt.movej(begin, acc=1, vel=0.3, wait = False) 
    burt.open_gripper()
    time.sleep(5)  

    burt.stream_data_start(0.01)
    time.sleep(1)
    burt.stream_data_stop(wait=False)
    time.sleep(1)
    print("Starting recording")
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,True,True))
    time.sleep(5)

    burt.movej(grip, acc=1, vel=0.4, wait = False) 
    time.sleep(2)
    burt.close_gripper()
    time.sleep(2)
    burt.movej(lift, acc=1, vel=0.4, wait = False)
    burt.movej(above, acc=1, vel=0.4, wait = False)
    burt.movej(down, acc=1, vel=0.4, wait = False)
    time.sleep(5)
    burt.open_gripper()
    time.sleep(1)
    burt.translatel_rel([0,0.1,0,0,0,0], acc=1, vel=0.2, wait = False)
    time.sleep(5)

    print("Ending recording")
    thread_flag = False
    time.sleep(3)


def shear1(burt, name='test'): 
    global thread_flag
    global pos_data
    burt.home()
    above = [-2.09147, -1.27578, 2.24879, -2.56293, -1.55631, 3.95426]
    touch = [-2.09147, -1.27211, 2.24973, -2.56751, -1.55645, 3.95428]
    burt.stream_data_start(0.01)
    time.sleep(1)
    burt.stream_data_stop(wait=False)
    time.sleep(1)
    print("Starting recording")
    _thread.start_new_thread(read_data,(burt,name,0,False,True,True,False,False))
    time.sleep(5)

    x_dist = 0.015
    y_dist = 0.02
    z_dist = 0.01
    # z_press_min = 0.002
    # z_press_max = 0.005 # in steps of one millimeter, this is 3 iterations
    # N = 3
    # z_press_delta = (z_press_max-z_press_min)/N
    # z_press = [-0.0005, 0, 0.0005, 0.001, 0.0015, 0.002]

    begin = -0.0005
    end = 0.002
    z_press = np.linspace(begin, end, 11)

    n = 75

    for j in range(len(z_press)):
        for i in range(n):
            print("Iteration {}/{} (z = {})".format(j*n+i,n*len(z_press),z_press[j]))
            burt.movej(above, wait = False)
            time.sleep(1)
            burt.movej(touch, wait = False)
            time.sleep(2)
            pos = np.array(copy.copy(pos_data))
            pos += np.array([0,0,-z_press[j],0,0,0])
            burt.movel(pos, acc=1, vel=0.01, wait = False)
            time.sleep(2)

            for k in range(7):
                pos = np.array(copy.copy(pos_data))
                pos += np.array([0,y_dist,0,0,0,0])
                burt.movel(pos, acc=1, vel=0.01, wait = False)
                time.sleep(2.5)

                pos = np.array(copy.copy(pos_data))
                pos += np.array([0,-y_dist,0,0,0,0])
                burt.movel(pos, acc=1, vel=0.01, wait = False)
                time.sleep(2.5)
                
                pos = np.array(copy.copy(pos_data))
                pos += np.array([0,0,z_dist,0,0,0])
                burt.movel(pos, acc=1, vel=0.05, wait = False)
                time.sleep(1)
                
                if k != 6:
                    pos = np.array(copy.copy(pos_data))
                    pos += np.array([-x_dist,0,0,0,0,0])
                    burt.movel(pos, acc=1, vel=0.05, wait = False)
                    time.sleep(1)
                    
                    pos = np.array(copy.copy(pos_data))
                    pos += np.array([0,0,-z_dist,0,0,0])
                    burt.movel(pos, acc=1, vel=0.05, wait = False)
                    time.sleep(1)

    print("Ending recording")
    pos = np.array(copy.copy(pos_data))
    pos += np.array([0,0,z_dist,0,0,0])
    burt.movel(pos, acc=1, vel=0.05, wait = False)
    burt.home()
    thread_flag = False
    time.sleep(3)

def wait_for_enter():
    global thread_flag
    thread_flag = True
    input()
    thread_flag = False
    return

def read_data_controller(burt,name,start_time=0,ft=True,pos=True,skin=True,cam=True,checkForHole=False):
    global thread_flag
    thread_flag = True
    global ft_data
    ft_data = [0,0,0,0,0,0]
    global pos_data
    pos_data = [0,0,0,0,0,0]
    global skin_data
    skin_data = []
    
    # global found_hole
    # global table_contact

    # def butter_lowpass(cutoff, nyq_freq, order=4):
    #     normal_cutoff = float(cutoff) / nyq_freq
    #     b, a = signal.butter(order, normal_cutoff, btype='lowpass')
    #     return b, a

    # def butter_lowpass_filter(data, cutoff_freq, nyq_freq, order=4):
    #     # Source: https://github.com/guillaume-chevalier/filtering-stft-and-laplace-transform
    #     b, a = butter_lowpass(cutoff_freq, nyq_freq, order=order)
    #     y = signal.filtfilt(b, a, data)
    #     return y

    path = 'Generic_ur5_controller/data/' + name
    Path(path).mkdir(parents=True, exist_ok=True)
    t = time.ctime().replace('  ','-').replace(' ','-').replace(':','.')
    name = path + '/' + t

    with open('{}_data.csv'.format(name), 'w', newline='') as csvfile:
        names = ['n']+['t']+['x','y','z','rx','ry','rz']+['fx','fy','fz','tx','ty','tz']+['skin']+['pinching']
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(names)
       
        n=0
        if cam == True:
            global cam_thread_flag
            _thread.start_new_thread(read_cam,(burt,name,start_time,))
        if ft == True:
            global ft_thread_flag
            _thread.start_new_thread(read_ft,(burt,start_time,))
        if pos == True:
           global pos_thread_flag
           _thread.start_new_thread(read_pos,(burt,start_time,False))
        time.sleep(1.2)
        # if skin == True:
        #     global skin_thread_flag
        #     _thread.start_new_thread(read_skin,(burt,start_time,))

        tic = time.time()
        # first = True
        # all_skin_data = []
        while thread_flag == True:
            current_time = time.time()-tic
            # if pos == True:
            #     pos_data = burt.getl()

            # if static_pos[0] != list(round(x,2) for x in pos_data):
            #     static_pos[0] = list(round(x,2) for x in pos_data)
            #     static_pos[1] = current_time
            # elif static_pos[0] == list(round(x,2) for x in pos_data) and current_time-static_pos[1]>10:
            #     thread_flag = False
            # else:
            #     pass

            # skin_ipt = burt.get_skin().replace("\r\n","").split("\t")
            # print(skin_ipt)
            
            print(burt.get_skin().replace("\r\n","").split("\t"))
            # skin_data = list(map(int, burt.get_skin().replace("\r\n","").split("\t")))

            
            # ###
            # # the following is just to stop at hole in table

            # all_skin_data.append(skin_data)
            # if len(all_skin_data) > 50:
            #     to_filter = np.transpose(np.array(all_skin_data))
            #     # print(np.shape(to_filter))
            #     filtered = []
            #     for f in to_filter:
            #         filtered.append(butter_lowpass_filter(f,1,10))
            
            #     if checkForHole:
            #         if table_contact:
            #             prev = [np.mean(s) for s in np.array(filtered)[:,-100:]] # 100 30 might work

            #             # if first:
            #             #     print('Collecting initial reference')
            #             #     prev = np.transpose(filtered)[-1]
            #             #     first = False
            #             if any(abs(prev-np.transpose(filtered)[-1]) > 30):
            #                 prev = np.array(np.transpose(filtered)[-1])
            #                 print('Detected sensor variation')
            #                 found_hole = True
            #         else: 
            #             first = True
            #     # print('found_hole: ', found_hole)
            # ###

            csvwriter.writerow([n,current_time]+pos_data+ft_data+skin_data+[pinching])
            n+=1

            # time.sleep(0.05)
            # print('in loop')

        ft_thread_flag = False
        pos_thread_flag = False
        skin_thread_flag = False
        cam_thread_flag = False
        time.sleep(1)
        #burt.stream_data_stop(wait=False)
        #burt.ee_force_stop()
        time.sleep(0.1)
        #burt.ee_stop_streaming()
        #burt.ping()
    return

def read_data(burt,name,start_time=0,ft=True,pos=True,skin=True,cam=True,checkForHole=False):
    global thread_flag
    thread_flag = True
    global ft_data
    ft_data = [0,0,0,0,0,0]
    global pos_data
    pos_data = [0,0,0,0,0,0]
    global skin_data
    skin_data = []

    path = 'Generic_ur5_controller/data/' + name
    Path(path).mkdir(parents=True, exist_ok=True)
    t = time.ctime().replace('  ','-').replace(' ','-').replace(':','.')
    name = path + '/' + t

    with open('{}_data.csv'.format(name), 'w', newline='') as csvfile:
        names = ['n']+['t']+['x','y','z','rx','ry','rz']+['fx','fy','fz','tx','ty','tz']+['skin']+['pinching']
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(names)
       
        n=0
        if cam == True:
            global cam_thread_flag
            _thread.start_new_thread(read_cam,(burt,name,start_time,))
        if ft == True:
            global ft_thread_flag
            _thread.start_new_thread(read_ft,(burt,start_time,))
        if pos == True:
           global pos_thread_flag
           _thread.start_new_thread(read_pos,(burt,start_time,False))
        time.sleep(1.2)

        tic = time.time()
        # first = True
        # all_skin_data = []
        while thread_flag == True:
            current_time = time.time()-tic
            
            # print(burt.get_skin().replace("\r\n","").split("\t")[:-1])
            skin_data = list(map(int, burt.get_skin().replace("\r\n","").split("\t")[:-1]))

            csvwriter.writerow([n,current_time]+pos_data+ft_data+skin_data+[pinching])
            n+=1

        ft_thread_flag = False
        pos_thread_flag = False
        skin_thread_flag = False
        cam_thread_flag = False
        time.sleep(1)
        #burt.stream_data_stop(wait=False)
        #burt.ee_force_stop()
        time.sleep(0.1)
        #burt.ee_stop_streaming()
        #burt.ping()
    return

def read_traj(burt,name='test',start_time=0,ft=True,pos=True,skin=True,cam=True):
    global thread_flag
    thread_flag = True
    global ft_data
    ft_data = [0,0,0,0,0,0]
    global pos_data
    pos_data = [0,0,0,0,0,0]
    global skin_data
    skin_data = []

    input("press enter to start and stop recording")
    _thread.start_new_thread(wait_for_enter,())

    with open('{}_{}_data.csv'.format(name,start_time), 'w', newline='') as csvfile:
        names = ['n']+['t']+['x','y','z','rx','ry','rz']+['fx','fy','fz','tx','ty','tz']+['skin']
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(names)
       
        n=0
        if cam == True:
            global cam_thread_flag
            _thread.start_new_thread(read_cam,(burt,name,start_time,))
        if ft == True:
            global ft_thread_flag
            _thread.start_new_thread(read_ft,(burt,start_time,))
        if pos == True:
            global pos_thread_flag
            _thread.start_new_thread(read_pos,(burt,start_time,True,))
        if skin == True:
            global skin_thread_flag
            _thread.start_new_thread(read_skin,(burt,start_time,))

        sequence = []
        time.sleep(0.1)
        sequence.append([pos_data,0,0])
        tic = time.time()
        prev_time = 0
        time.sleep(0.1)
        while thread_flag == True:
            current_time = time.time()-tic
            timestep = current_time-prev_time
            csvwriter.writerow([n,current_time]+pos_data+ft_data+skin_data)
            sequence.append([pos_data,timestep,0])
            n+=1
            prev_time = current_time
            time.sleep(0.1)

        print(n)
        ft_thread_flag = False
        pos_thread_flag = False
        skin_thread_flag = False
        cam_thread_flag = False
        sequence.append([pos_data,time.time()-tic,0])
        time.sleep(0.5)
        open('{}_{}_traj.json'.format(name,start_time), "w").write(json.dumps(sequence))
        burt.socket_send(burt.format_prog(31))
        burt.stream_data_stop()
        burt.ee_force_stop()
        time.sleep(0.1)
        burt.ee_stop_streaming()
        burt.ping()
    return 

def play_and_read(burt, name, ft=False, pos=True, skin=True, cam=True, rp=0):
    sequence = json.load(open(name))
    print(len(sequence))
    print("average timestep: ",sequence[-1][1]/(len(sequence)-2))
    
    burt.movel(sequence[0][0])

    start_time = int(time.time())
    name = name.split('.')[0]+'_replay{}'.format(rp)
    global thread_flag
    _thread.start_new_thread(read_data,(burt,name,start_time,ft,pos,skin,cam))
    
    toc = time.time()
    for i in range(1,len(sequence)-1):
        burt.set_digital_out(0,sequence[i][2])
        burt.servoj(sequence[i][0],control_time=sequence[i][1],lookahead_time=0.008,gain=300)

    burt.stopl(0.5)
    thread_flag = False
    tic = time.time()
    time.sleep(0.5)
    burt.ping()
    #burt.socket_flush()
    print("recorded ",sequence[-1][1],"secs")
    print("executed in ",tic-toc,"secs")
    print("recorded end_pos: ",sequence[-1][0])
    print("actual end_pos:",burt.getl())

def read_ft(burt,start_time):
    global ft_thread_flag
    ft_thread_flag = True
    global ft_data
    ft_data = [0,0,0,0,0,0]

    print('ft data start')

    while ft_thread_flag == True:
        ft_data = burt.ft.read()
        time.sleep(0.01)
    return

def read_pos(burt,start_time,fd):
    global pos_thread_flag
    pos_thread_flag = True
    global pos_data
    pos_data = [0,0,0,0,0,0]
    # global thread_flag

    static_detector = []

    # print('pos data start')
    burt.ping()
    if fd==True:
        burt.socket_send(burt.format_prog(30))
    burt.stream_data_start(0.01)
    while pos_thread_flag == True:
        try:
            raw = burt.read_msg()
            # print(raw)
            if raw != []:
                pos_data = raw    
        except:
            pass
    return

def read_skin(burt,start_time):
    global skin_thread_flag
    skin_thread_flag = True
    global skin_data
    skin_data = []

    print('skin data start')

    # burt.ee_start_streaming()
    while skin_thread_flag == True:
        raw = bytes.decode(burt.ee.readline())
        skin_data = []
        # print(type(raw))
        # print(raw)

        n = 0
        for item in raw[0:-1].split("\t"):
            if item == 'S':
                n = 1
            elif n == 1:
                # time = float(item)
                n = 0
            else:
                skin_data.append(float(item))
        time.sleep(0.05)
    return

def read_cam(burt,name,start_time):
    global cam_thread_flag
    cam_thread_flag = True

    filename = "{}_{}_vid.avi".format(name,start_time)
    cap = cv2.VideoCapture(1,cv2.CAP_DSHOW )
    cap.set(cv2.CAP_PROP_AUTOFOCUS,0)
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'XVID'), 25, (640, 480))# [1920, 1080])
    ret, frame = cap.read()
    cv2.imwrite('{}_{}_start.jpg'.format(name,start_time), frame)

    while cam_thread_flag == True:
        ret, frame = cap.read()
        out.write(frame)

    ret, frame = cap.read()
    cv2.imwrite('{}_{}_end.jpg'.format(name,start_time), frame)


    cap.release()
    out.release()    
    cv2.destroyAllWindows()
    return
