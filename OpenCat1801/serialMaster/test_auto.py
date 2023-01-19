#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
sys.path.append("..")
from ardSerial import *
from SR04 import *

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
