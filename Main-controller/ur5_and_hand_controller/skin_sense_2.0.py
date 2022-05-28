import time
import numpy as np
import _thread
import csv
from pathlib import Path
from threading import Thread
from queue import Queue
import time

import kg_robot as kgr

ft_data = []
pos_data = []
skin_data = []

class skin_sense():
    def __init__(self,robot):
        self.robot = robot

def table1(burt,angles,name='test'):

    base = [-0.140,-0.534,0.374,0.49,1.082,-2.254]

    burt.ee_start_streaming()
    thread1 = Thread( target=read_data, args=(burt,name,0,True,True,True,True) )
    thread1.start()

    burt.movel(base, wait = False)
    time.sleep(0.5)
    burt.movel([-0.140,-0.534,0.31,0.49,1.082,-2.254],wait = False)
    burt.movel_tool([0,0,0,0,0,angles[2]], acc=0.1, vel=0.1, wait = False)
    burt.movel_tool([0,0,0,angles[0],angles[1],0], acc=0.1, vel=0.1, wait = False)
    time.sleep(5)
    burt.movel(base, wait = False)
    time.sleep(1)

    burt.ee_stop_streaming()
    thread1.join()

def read_data(burt,name,start_time=0,ft=True,pos=True,skin=True,cam=True):
    ft_data = [0,0,0,0,0,0]
    pos_data = [0,0,0,0,0,0]
    skin_data = []

    path = 'Generic_ur5_controller/csv_files/' + name
    Path(path).mkdir(parents=True, exist_ok=True)
    t = time.ctime().replace('  ','-').replace(' ','-').replace(':','.')
    name = path + '/' + t

    with open('{}_{}_data.csv'.format(name,start_time), 'w', newline='') as csvfile:
        names = ['n']+['t']+['x','y','z','rx','ry','rz']+['fx','fy','fz','tx','ty','tz']+['skin']
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(names)
       
        n=0
        tic = time.time()
        while True:
            current_time = time.time()-tic
            if pos == True:
                pos_data = burt.getl()
            skin_data = list(map(int, burt.get_skin().replace("\r\n","").split("\t")))
            csvwriter.writerow([n,current_time]+pos_data+ft_data+skin_data)
            n+=1
            time.sleep(0.1)

    return
