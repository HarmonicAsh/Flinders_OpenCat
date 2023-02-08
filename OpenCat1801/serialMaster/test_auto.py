#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#Req pyserial and pip3
#sudo apt-get install python3-tk
#Use to install Pip3 as req: sudo apt-get -y install python3-pip

#https://wavlist.com/animals-cats-20-wavs/ cat sounds found here <-


import sys
import time
sys.path.append("..")
from ardSerial import *
from SR04 import *

def direction():
        print("---------------------changing direction---------------------------")
        send(goodPorts,['ksit',0.5],)  #Sit, then look straight ahead and measure the distance to the obstruction
        send(goodPorts,['i', [0, 0, 1, -30], 0.5],)
        dist = distance() 
        print("The obstruction is... ")
        print(dist, " cm in front")
        send(goodPorts,['i', [0, 50, 1, -38], 0.5],) #Look left and measure the distance to the obstruction
        dist_left = distance()
        print(dist_left, " cm to the left")
        send(goodPorts,['i', [0, -50, 1, -38], 0.5],) #Look right and measure the distance to the obstruction
        dist_right = distance()
        print(dist_right, " cm to the right")
          
        if dist_left < dist_right:      #When Nybble should deviate right
            time_mod = dist_left/dist_right
            print("Time factor (face right) = ", time_mod)
            send(goodPorts,['kbkL',0],)
            
        elif dist_left > dist_right:        #When Nybble should deviate ;eft   
            time_mod = dist_right/dist_left
            print("Time factor (face left) = ", time_mod)   
            send(goodPorts,['kbkR',0],)

        else: #If the same reading is recorded (in case of error, should not be possible)
            print("These measurements don't make sense... potential ultrasonic sensor error")
            send(goodPorts,['kbalance',2],)
            send(goodPorts,['krest',10],) 
            motion()
        
        time.sleep(3)                        #Prevents getting stuck in a loop of rechecking distances
        for i in range(round(25*time_mod)):  #Re-orient position and recheck distance throughout progress
            dist = distance()
            if dist <= 24:
                direction()
            else:
                time.sleep(0.25)
                pass
        print("------------------------------------------------------------------")
        motion()
             
       

def Nybble_sleep(): #Shuts down Nybble when the script has finished
        print("\nTerminating... farewell!")
        send(goodPorts,['krest',1],)  #Rest
        closeAllSerial(goodPorts)
        logger.info("finish!")
        os._exit(0)

def motion():
        dist = distance() #Need to add some form of error checking here!
        send(goodPorts,['kwkF',0.1],)
        while dist >= 24:
            dist = distance()
            print("Distance = ", dist, "cm")
            time.sleep(0.1)
            #read_inputs() want the cat to constantly read for inputs, so that we can terminate the process!
        else:
            direction()
            
def start_cat():
        send(goodPorts,['d',0],) # rest position and shuts off all servos
        print("\n \n------------------------------------------------------------------")
        print("Welcome to the Flinders OpenCat project. Enter a command to begin!") 
        print("------------------------------------------------------------------")
        print("'go'' to commence automated motion") 
        print("'dist' prints ulstrasonic sensor measured distance for 10 seconds") 
        print("'serial' to use Petoi commands directly as a serial input") 
        print("'quit' to terminate...") 
        print("'test' to operate the function test() as required") 

def test():
        dist = distance() 
        print("---------------------changing direction---------------------------")
        send(goodPorts,['ksit',0.5],)  #Sit, then look straight ahead and measure the distance to the obstruction
        send(goodPorts,['i', [0, 0, 1, -30], 0.5],)
        print("The obstruction is... ")
        print(dist, " cm in front")
        send(goodPorts,['i', [0, 50, 1, -38], 0.5],) #Look left and measure the distance to the obstruction
        dist_left = distance()
        print(dist_left, " cm to the left")
        send(goodPorts,['i', [0, -50, 1, -38], 0.5],) #Look right and measure the distance to the obstruction
        dist_right = distance()
        print(dist_right, " cm to the right")
          
        if dist_left < dist_right:      #When Nybble should deviate right
            time_mod = dist_left/dist_right
            print("Time factor (face right) = ", time_mod)
                        
        elif dist_left > dist_right:        #When Nybble should deviate ;eft   
            time_mod = dist_right/dist_left
            print("Time factor (face left) = ", time_mod)   
            
        else:
            pass
        
        print("------------------------------------------------------------------") 
        print("Test completed..")
        
def read_inputs():
        command = input() #Reads serial inputs
        if command == "go":
                print("\nGo command recognised... let's go!")
                send(goodPorts,['u',1],) 
                send(goodPorts,['kbalance',1],)  #Stand up and wait for 1 second
                motion()  #Start walking forwards and attempt to avoid walls

        elif command == "dist": #prints the distance signal of the ultrasonic sensor
                print("\nMeasured distance (centimetres)")
                for i in range(10):
                    print(distance()) 
                    time.sleep(1)
                start_cat()

        elif command == "test": #Runs test() once
                print("\nRunning test()")
                test()
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
        time.sleep(1)
        send(goodPorts,['g',0],)# switch gyroscope on (begins off)
        send(goodPorts,['d',1],) # rest position and shuts off all servos
        send(goodPorts,['z',1],) # disable random behaviour
        start_cat()
        
        while True:
            read_inputs()
        
        
    except Exception as e:
        logger.info("Exception")
        closeAllSerial(goodPorts)
        os._exit(0)
        raise e