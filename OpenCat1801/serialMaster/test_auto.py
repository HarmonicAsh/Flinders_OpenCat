#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import time
sys.path.append("..")
from ardSerial import *
from SR04 import *

def direction():
        dist = direction() 
        #Sit when an object appears too close
        print("I am too close to something...")
        send(goodPorts,['ksit',1],)
        send(goodPorts,['kbalance', 1],)
                
        #Look straight ahead and measure the distance to the obstruction
        send(goodPorts,['i', [0, 0, 1, 0], 1],)
        print("Looking straight")
        print("Straight ahead: ", dist, " cm")
        time.sleep(1)

        #Look left and measure the distance to the obstruction
        send(goodPorts,['i', [0, 45, 1, -40], 1],) #Look left
        time.sleep(1)
        dist_left = dist
        print("Distance left: ", dist, " cm")
        send(goodPorts,['i', [0, -50, 1, 0], 0],)
        
        #Look right and measure the distance to the obstruction
        send(goodPorts,['i', [0, -45, 1, -40], 1],)
        time.sleep(1)
        dist_right = dist
        print("Distance right: ", dist, " cm")

        #Choose which way to face
        print("Time to find a way around this obstruction...")
        
        #When Nybble should deviate right
        if dist_left < dist_right:
            time_mod = dist_left/dist_right
            time = 2*time_mod
            send(goodPorts,['kbkL',time],)  
            send(goodPorts,['kbalance',1],)
            send(goodPorts,['kwkF',10],)
            
        
        #When Nybble should deviate left
        if dist_left > dist_right:    
            time_mod = dist_right/dist_left
            time = 2*time_mod
            send(goodPorts,['kbkR',time],) 
            send(goodPorts,['kbalance',1],)
            send(goodPorts,['kwkF',10],)

        #If the same reading is recorded (in case of error, should not be possible)
        else:
            send(goodPorts,['kbalance',2],)
            send(goodPorts,['krest',10],) 

def Nybble_sleep(): #Shuts down Nybble when the script has finished
        print("stop command recognised..")
        send(goodPorts,['krest',1],)  #Rest
        closeAllSerial(goodPorts)
        logger.info("finish!")
        os._exit(0)

def motion():
        print("Beginning motion function... ")
        dist = distance()
        send(goodPorts,['kwkF',1],)
        while dist >= 6:
            dist = distance()
            print("Forwards...")
            print("Distance = ", dist, "cm")
            time.sleep(1)
        else:
            direction()
            
def start_cat():
        send(goodPorts,['d',0],) # rest position and shuts off all servos
        print("\n \nWelcome to the Flinders OpenCat project. Enter a command to begin!") 
        print("------------------------------------------------------------------")
        print("'go'' to commence automated motion") 
        print("'dist' prints ulstrasonic sensor measured distance for 10 seconds") 
        print("'serial' to use Petoi commands directly as a serial input") 
        print("'quit' to terminate...") 

if __name__ == '__main__':
    try:
        '''
        testSchedule is used to test various serial port commands
        '''
        print("Let's see if this repeats..")
        goodPorts = {}
        connectPort(goodPorts)
        t=threading.Thread(target = keepCheckingPort, args = (goodPorts,))
        t.start()
        parallel = False
        time.sleep(1)
        #send(goodPorts,['g',0],)# switch gyroscope on (begins off)
        send(goodPorts,['d',1],) # rest position and shuts off all servos
        start_cat()
        
        while True:
            command = input() #Reads serial inputs

            if command == "go":
                print("go command recognised... let's go!")
                send(goodPorts,['kbalance',1],)  #Stand up and wait for 1 second
                motion()  #Start walking forwards and attempt to avoid walls

            elif command == 'dist': #prints the distance signal of the ultrasonic sensor
                print("\nMeasured distance (centimetres)")
                for i in range(10):
                    print(distance()) 
                    time.sleep(1)
                start_cat()

            elif command == "serial": #allows the input of Petoi serial commands
                serial_comm = 1
                while serial_comm == 1:
                    print("\nWaiting for a Petoi serial command... back to return, quit to exit")
                    command = input()
                    if command == "quit": #Terminate the code
                        Nybble_sleep() 
                    elif command == "back": #Return to main command meny
                        start_cat()
                        serial_comm = 0
                    else: 
                        send(goodPorts,[command,0],) #Sends an input directly to Nybble. Use Petoi documentation for commands
                        time.sleep(0.2)

            elif command == "quit":
                Nybble_sleep() #Terminate the code
        print("Do we ever reach this line?")

    except Exception as e:
        logger.info("Exception")
        closeAllSerial(goodPorts)
        os._exit(0)
        raise e