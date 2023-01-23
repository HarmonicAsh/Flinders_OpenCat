#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import time
sys.path.append("..")
from ardSerial import *
from SR04 import *

def direction():
    dist = distance()
    if dist <= 20:
        #Sit when an object appears too close
        print("I am too close to something...")
        send(goodPorts,['ksit',1],)  
        
        #Look straight ahead and measure the distance to the obstruction
        send(goodPorts,['M', ['M', '0', '0', '1', '0'], 1],) #Look straight ahead
        print("Straight ahead: ", dist, " cm")
        time.sleep(0.25)

        #Look left and measure the distance to the obstruction
        send(goodPorts,['M', ['M', '0', '-45', '1', '0'], 1],) #Look left
        time.sleep(0.25)
        dist_left = dist
        
        #Look right and measure the distance to the obstruction
        send(goodPorts,['M', ['M', '0', '45', '1', '0'], 2],) 
        time.sleep(0.25)
        dist_right = dist

        #Choose which way to face
        print("Time to find a way around this obstruction...")

        #When Nybble should deviate left
        if dist_left < dist_right:      
            send(goodPorts,['kbkL',2],)  
            send(goodPorts,['kbalance',10],)  
        
        #When Nybble should deviate right
        if dist_left > dist_right:      
            send(goodPorts,['kbkR',2],) 
            send(goodPorts,['kbalance',10],)  

        #If the same reading is recorded (in case of error, should not be possible)
        else:
            send(goodPorts,['kbalance',2],)
            send(goodPorts,['krest',10],) 

def Nybble_sleep(): #Shuts down Nybble when the script has finished
        send(goodPorts,['krest',1],)  #Rest
        closeAllSerial(goodPorts)
        logger.info("finish!")
        os._exit(0)

def motion():
        print(distance())
        print("Walking forwards...")
        send(goodPorts,['kwkF',0],)
        direction()
        motion()
if __name__ == '__main__':
    try:
        '''
        testSchedule is used to test various serial port commands
        '''
         #Connect to the Nyboard
        goodPorts = {}
        connectPort(goodPorts)
        t=threading.Thread(target = keepCheckingPort, args = (goodPorts,))
        t.start()
        parallel = False
        #if len(goodPorts)>0:
        time.sleep(1);
        #send(goodPorts,['p',0],)# pause and shut off servos
        #send(goodPorts,['g',0],)# switch gyroscope on (begins off?)
        send(goodPorts,['d',0],)# rest and shut off servos
        print("Enter 'go' to begin, 'dist' to test ultrasonic sensor, 'quit' or 'stop' to terminate...") 
        
        #Carry out motions and allow termination
        while True:
            command = input() #Reads serial inputs
            if command == "go":
                print("go command recognised... let's go!")
                send(goodPorts,['kbalance', 1],)
                motion()  #Wait 5s, walk forwards until obstruction, change course
            elif command == 'dist':
                print(distance())
                time.sleep(0.2)
            elif command == "direct":
                print("direct command recognised. Input serial commands directly.")
                Nybble_sleep() #Terminate the code
            elif command == "stop" or "quit":
                print("stop command recognised..")
                Nybble_sleep() #Terminate the code
       
    except Exception as e:
        logger.info("Exception")
        closeAllSerial(goodPorts)
        os._exit(0)
        raise e