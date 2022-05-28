import _thread
from calendar import c
import copy
import csv
import time
import random
import math

#import nidaqmx
import numpy as np
import scipy.optimize as optimize
import serial

import kg_robot as kgr
import waypoints as wp
import skin_sense as ss

def main():
    print("------------Configuring Burt-------------\r\n")
    burt = kgr.kg_robot(port=30010,ee_port="COM9",db_host="169.254.88.130")
    # burt = kgr.kg_robot(ee_port="COM9")
    print("----------------Hi Burt!-----------------\r\n\r\n")

    ipt = input("For previous home position type p, to update the home to current position type c: ")
    if ipt == 'p':
        print("Previous home position:")
    if ipt == 'c':
        wp.burt_homej = burt.getj()
        print('New home position (copy manually to waypoints):')
    print(wp.burt_homej)
    burt.home(pose = wp.burt_homej, wait=False)

    name = ''
    try:
        while 1:
            ipt = input("cmd: ")

            if ipt == 'flush':
                burt.socket_flush()

            if ipt == 't':
                name = burt.skin.record(ft=False,pos=True,skin=True,cam=True)
                print(name)
            if ipt == 'play':
                if name=='':
                    name = input('name: ')
                burt.skin.play(name,ft=False,pos=True,skin=True,cam=True)

            if ipt == 's0':
                #burt.ee_stop_streaming()
                burt.serial_send('S',0)
            if ipt == 's1':
                #burt.ee_start_streaming()
                burt.serial_send('S',1)
            if ipt == 'cl':
                burt.ee.reset_input_buffer()
            if ipt == 'r':
                print(bytes.decode(burt.ee.readline()))

            if ipt == 'read':                
                print(list(map(int, burt.get_skin().replace("\r\n","").split("\t"))))
            
            if ipt == 'rate':
                N = 100
                start = time.time()
                for _ in range(N):
                    print(burt.get_skin())
                end = time.time()
                print('total time: ' + str(end - start))
                print('rate = {} Hz'.format(N/(end - start)))
            
            if ipt == 'c':
                with open('test.csv', 'w', newline='') as csvfile:
                    names = ['test1','test2','test3']
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(names)
                    for row in range(1,10):
                        csvwriter.writerow([row,row+1,row+2])

            if ipt == 'a':               
                ss.test(burt)

            if ipt == 'servo_close':
                burt.close_gripper()
            
            if ipt == 'servo_open':
                burt.open_gripper()

            if ipt == 'chop':
                for _ in range(10):
                    ang = random.uniform(0, 360)
                    ss.chopstick1(burt, ang, 'test2')

            if ipt == 'table1':
                for _ in range(5):
                    a1 = np.array([0,0,1])
                    a2 = np.array([1/math.sqrt(2),-1/math.sqrt(2),0])
                    r1 = a1 * (random.uniform(-15, 15) * math.pi /180)
                    r2 = a2 * (random.uniform(-15, 15) * math.pi /180)

                    ss.table1(burt, r1+r2, 'test6')
            
            if ipt == 'table2':
                ss.table2(burt, 'orientation-repeat')

            if ipt == 'table3':
                ss.table3(burt, 'cam2')

            if ipt == 'c2':
                ss.chopstick2(burt, 'angle1')

            if ipt == 'c4':
                ss.chopstick4(burt, 'rename-me')
            
            if ipt == 'c5':
                ss.chopstick5(burt, 'test7')

            if ipt == 'c6':
                ss.chopstick6(burt, 'cantilever1')

            if ipt == 'pick':
               ss.pick_up(burt, 'test10-open-close')

            if ipt == 'contour1':
               ss.contour1(burt, 'contour1')

            if ipt == 'contour2':
               ss.contour2(burt, 'contour2')

            if ipt == 'contour3':
               ss.contour3(burt, 'contour3')
            
            if ipt == 'freq1':
               ss.freq1(burt, 'freq1')

            if ipt == 'speed1':
               ss.speed1(burt, 'speed1')

            if ipt == 'hole1':
               ss.find_hole1(burt, 'hole1')
            
            if ipt == 'hole2':
               ss.hole2(burt, 'hole2')

            if ipt == 'min_ang':
               ss.min_angle1(burt, 'min_angle1')

            if ipt == 'rep':
               ss.rep(burt, 'repeatability')

            if ipt == 't1':
               ss.tau1(burt, 'tau1')

            if ipt == 't2':
               ss.tau2(burt, 'tau2')
                           
            if ipt == 'rec':
               ss.simple_record(burt, 'recording_impulse')
               
            if ipt == 'demo':
                ss.demo_IROS_pick(burt, 'demo_IROS_hole')

            if ipt == 'shear1':
                ss.shear1(burt, 'shear1')

            if ipt == 'close':
                break
            elif ipt == 'home':
                burt.home()

            
            #else:
            #    var = int(input("var: "))
            #    burt.serial_send(ipt,var,True)

        
    finally:
        print("Goodbye")
        burt.close()
if __name__ == '__main__': main()



