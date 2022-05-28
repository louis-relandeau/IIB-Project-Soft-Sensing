import time
import serial
from math import pi
import numpy
import socket
import keyboard

import waypoints as wp
import kg_robot as kgr
# This needs to be updated, no longer working !!!!
import sensing_hand_arduino as hand


def main():
    print("------------Configuring Burt-------------\r\n")
    burt = kgr.kg_robot(port=30010,db_host="169.254.185.30")
    print("----------------Hi Burt!-----------------\r\n")

    print("------------Connecting to Hand-------------\r\n")
    try:
        arduino = serial.Serial(port="COM9", timeout=1, baudrate=115200)
        print("Successfully connected to Arduino\r\n")
    except:
        print('Not connected to board. Check port...')

    try:
        while 1:
            ipt = input("cmd: ")
            if ipt == 'close':
                break
            elif ipt == 'home':
                burt.home()
            elif ipt == 'rec':
                burt.teach_mode.record()
            elif ipt == 'play':
                burt.teach_mode.play()

            elif ipt == 'vel':
                burt.speedl([0,0,-0.01,0,0,0],acc=0.1,blocking_time=5)

            elif ipt == 'hi':
                burt.set_digital_out(0,1)
            elif ipt == 'lo':
                burt.set_digital_out(0,0)

            elif ipt == 'data':
                while True:  
                    try:  
                        hand.read_sensors(arduino)
                        if keyboard.is_pressed(' '):
                            break 
                    except:
                        pass
            elif ipt == 'servo':
                hand.move_servo(arduino)
            elif ipt == 'down':
                burt.movel([-0.1259,-0.3339,0.1672,0.0937,2.753,-1.263])
            elif ipt == 'up':
                burt.movel([-0.1259,-0.3339,0.2672,0.0937,2.753,-1.263])
            elif ipt == 'position':
                print(burt.getl())

            elif ipt == 'demo':
                burt.movel([-0.1259,-0.3339,0.1672,0.0937,2.753,-1.263])
                time.sleep(0.5)
                hand.move_servo(arduino)
                time.sleep(2)
                burt.movel([-0.1259,-0.3339,0.3172,0.0937,2.753,-1.263])
                time.sleep(2)
                burt.movel([-0.1259,-0.3339,0.1672,0.0937,2.753,-1.263])
                time.sleep(0.5)
                hand.move_servo(arduino)
                time.sleep(2)
                burt.home()


            else:
                var = int(input("var: "))
                burt.serial_send(ipt,var,True)

        
    finally:
        print("Goodbye")
        burt.close()
if __name__ == '__main__': main()
