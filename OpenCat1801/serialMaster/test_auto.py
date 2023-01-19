#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
sys.path.append("..")
from ardSerial import *
from SR04 import *

def direction():
    dist = distance()
    if dist <= 100:
        print("I am too close to something...")
        send(goodPorts,['ksit',1],)  #Sit when an object appears too close
        send(goodPorts,['m', ['0', '0', '1', '10'], 1],) #Look straight ahead
        sleep(0.25)
        send(goodPorts,['m', ['0', '-45', '1', '0'], 1],) #Look left
        dist_left = dist
        sleep(0.25)
        send(goodPorts,['m', ['0', '45', '1', '0'], 2],) #Look right
        dist_right = dist
        print("Time to find a way around this obstruction...")
        if dist_left < dist_right:
            send(goodPorts,['kbkL',2],)  #Back up and face the right
            send(goodPorts,['kbalance',10],)  #Stand for a while
        if dist_left > dist_right:
            send(goodPorts,['kbkR',2],)  #Back up and face the left
            send(goodPorts,['kbalance',10],)  #Stand for a while
        else:
            send(goodPorts,['kbalance',2],)  #Back up
            send(goodPorts,['krest',10],)  #Rest, let's not be defeated by this

if __name__ == '__main__':
    try:
        '''
        testSchedule is used to test various serial port commands
        '''
        goodPorts = {}
        connectPort(goodPorts)
        t=threading.Thread(target = keepCheckingPort, args = (goodPorts,))
        t.start()
        parallel = False
#        if len(goodPorts)>0:
        time.sleep(2);
        #INSERT HERE, COMMANDS TO BYPASS TESTSCHEDULE
        print(distance())
        direction()
        send(goodPorts,['g',0],)# switch gyroscope
        send(goodPorts,['z',0],)# switch random behavior
        send(goodPorts,['kwkF',4],)   
        send(goodPorts,['ksit',4],) 
#        schedulerToSkill(goodPorts, testSchedule) # compile the motion related instructions to a skill and send it to the robot. the last skill sent over in this way can be recalled by the 'T' token even after the robot reboots.
        closeAllSerial(goodPorts)
        logger.info("finish!")
        os._exit(0)

    except Exception as e:
        logger.info("Exception")
        closeAllSerial(goodPorts)
        os._exit(0)
        raise e
