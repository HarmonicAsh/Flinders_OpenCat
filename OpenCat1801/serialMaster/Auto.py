#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#Req pyserial and pip3
#sudo apt-get install python3-tk
#Use to install Pip3 as req: sudo apt-get -y install python3-pip
#https://wavlist.com/animals-cats-20-wavs/ cat sounds found here <-


import random
import sys
import time
import math
from pygame import mixer
sys.path.append("..")
from ardSerial import *
from SR04 import *
        
         
def load_sound():
        mixer.init()  #Initialise pigame mixer for audio
        print("Loading sounds...")
        global cat1
        global cat2
        global cat3
        global cat4
        global cat5
        cat1 = mixer.Sound("cat1.wav")   #load wav files
        cat2 = mixer.Sound("cat2.wav")   #load wav files
        cat3 = mixer.Sound("cat3.wav")   #load wav files
        cat4 = mixer.Sound("cat4.wav")   #load wav files
        cat5 = mixer.Sound("cat5.wav")   #load wav files
        print("Loading sounds completed.\n") #Load_sound (Loads sounds for the cat to "play")

def direction():
        print("\n---------------------changing direction---------------------------")
        send(goodPorts,['ksit',0.5],)  #Sit, then look straight ahead and measure the distance to the obstruction
        send(goodPorts,['i', [0, 0, 1, -30], 0.5],)
        time.sleep(0.25)
        dist = distance()
        print("Distance (non-averaged) = ", dist)
        if dist >= 60:
            print("The obstruction appears to have moved...")
            random_behaviour()
            motion()
        else:
            print("The obstruction is... ")
            print(dist, " cm in front")
            send(goodPorts,['i', [0, 50, 1, -38], 0.5],) #Look left and measure the distance to the obstruction
            global dist_left 
            dist_left = distance()
            print(dist_left, " cm to the left")
            send(goodPorts,['i', [0, -50, 1, -38], 0.5],) #Look right and measure the distance to the obstruction
            global dist_right
            dist_right = distance()
            print(dist_right, " cm to the right")
            send(goodPorts,['i', [0, 0, 1, -30], 0.5],)
            dist = distance()
            print("Distance (non-averaged) = ", dist)

        if dist >= 60:
            motion()
        elif dist_left < dist_right:
            print("Going right..")
            time_mod = 0.5+1*dist_left/dist_right
            print("Time delay = ", time_mod)
            cat_meow(random.randint(0,2))
            right_until(time_mod)
            
        elif dist_left > dist_right:
            print("Going left..")
            time_mod = 0.5+1*dist_right/dist_left
            print("Time delay = ", time_mod)
            cat_meow(random.randint(0,2))
            left_until(time_mod)
        else:
            print("These measurements don't make sense... check ultrasonic sensor")
            send(goodPorts,['kbalance',2],)
            send(goodPorts,['krest',1],)
            Nybble_sleep()      

        print("------------------------------------------------------------------\n")
        motion() #Direction (Code for the cat to measure distances to decide which direction to turn in)

def random_behaviour():
        behaviour = random.randint(0,7)
                
        cat_meow(random.randint(0,4))
        if behaviour == 0:
            send(goodPorts,['kstr',0],)
        elif behaviour == 1:
            send(goodPorts,['kbuttUp',0],)
        elif behaviour == 2:
            send(goodPorts,['kstr',0],)
            send(goodPorts,['kbuttUp',1],)
        elif behaviour == 3:
            send(goodPorts,['kck',0],)
        elif behaviour == 4:
            send(goodPorts,['kck',0],)
            send(goodPorts,['kbk',1],)
            cat_meow(random.randint(0,2))
            send(goodPorts,['kstr',0],)
        elif behaviour == 5:
            pass
        elif behaviour == 6:
            send(goodPorts,['kvt',3],) #Random_behaviour (Code for the cat to randomly "behave" differently, when presented with an obstruction)

def cat_meow(int):
        if int == 0:
            mixer.Sound.play(cat1)
        elif int == 1:
            mixer.Sound.play(cat2)
        elif int == 2:
            mixer.Sound.play(cat3)
        elif int == 3:
            mixer.Sound.play(cat4)
        elif int == 4: #File 4 currently has problems, using 3 again instead    
            mixer.Sound.play(cat3) #Cat_meow (Use to make the cat meow)   
            
def right_until(int):        
        dist = distance()
        send(goodPorts,['kbkL',int],)
        while dist <=60:
            time.sleep(0.2)
            dist = dist_av()
        motion() #Right_until (The cat will turn right until the obstruction is nolonger detected)

def left_until(int):
        dist = distance()
        send(goodPorts,['kbkR',int],)
        while dist <= 60:
            time.sleep(0.2)
            dist = dist_av()
        motion() #Left_until (The cat will turn left until the obstruction is nolonger detected)

def Nybble_sleep(): #Shuts down Nybble when the script has finished
        print("\nTerminating... farewell!")
        send(goodPorts,['krest',1],)  #Rest
        closeAllSerial(goodPorts)
        logger.info("finish!")
        os._exit(0) #Nybble_sleep (Puts the cat into a shutdown state)

def motion():
        global speed
        global speed_mod

        if speed == "1":
            print("attempting speed 1")
            speed_mod = 2
            send(goodPorts,['kcrF',1],)           
        elif speed == "2":
            print("attempting speed 2")
            speed_mod = 2
            send(goodPorts,['kwkF',1],)
        elif speed == "3":
            print("attempting speed 3")
            speed_mod = 0.5
            send(goodPorts,['ktrF',1],)

        dist = dist_av()

        while dist >= 20:
            dist = dist_av()
            time.sleep(0.01)            
        else:
            direction() #Motion (Starts the cat moving forwards, based on speed setting)


def start_cat():
        send(goodPorts,['d',0],) # rest position and shuts off all servos
        print("\n \n------------------------------------------------------------------")
        print("Welcome to the Flinders OpenCat project. Enter a command to begin!") 
        print("------------------------------------------------------------------")
        print("'go'' to commence automated motion") 
        print("'dist' prints ulstrasonic sensor measured distance for 10 seconds") 
        print("'serial' to use Petoi commands directly as a serial input") 
        print("'sound' to test sound output") 
        print("'quit' to terminate...") 
        print("'test' to operate the function test() as required") #Start cat function (lists main menu options)


def audio_test():
        for i in range(4):
            print("Testing meow number ", i)
            cat_meow(i)
            time.sleep(2) #Test_audio (Tests the playback of audio)

def dist_init():
        global dist_arr
        global arr_pos
        dist_arr = [0, 0, 0, 0, 0]
        send(goodPorts,['kbalance',1],)  #Stand up and wait for 1 second
        for x in range(5):
            dist_arr[x] = distance()
            time.sleep(0.1)
        print("[ ",dist_arr[0]," ",dist_arr[1]," ",dist_arr[2]," ",dist_arr[3]," ",dist_arr[4], " ] ")
        time.sleep(1)
        print("Array full..")
        arr_pos = 0
        total = 0
        #return dist_add(arr_pos, dist_arr)    #to call:   dist, arr_pos, dist_arr = dist_init(arr_pos,dist_arr)
        #return arr_pos, dist_arr  # to call: arr_pos, 
        
def dist_av():
        global dist_arr
        global arr_pos
        total = 0
        dist_arr[arr_pos] = distance()
        for i in range(5):
            total += dist_arr[i]
        dist = total/5
        print("Distance = ", dist, "cm")
        time.sleep(0.0025)
        arr_pos += 1
        if arr_pos == 5:
            arr_pos = 0
        else:
            pass
        return dist
       # return dist, arr,pos, dist_arr   # to call:     dist, arr_pos, dist_arr = dist_add(arr_pos,dist_arr)
        

def test():
        dist_init()
        while True:
            dist_av()
            time.sleep(1) #Test (Add code here for simpler testing)   
        
def gyro_toggle(int):
        print("Running gyroscope toggle")
        if int == 3: #Initial setup
            global gyro_status 
            send(goodPorts,['g',0],)# toggle gyroscope (increases cat speed)
            gyro_status = 1
            print("Gyroscope activated (enabled)")

        if int == 0:
            if gyro_status == 0:
                print("Gyroscope already inactive")
                
            else:
                send(goodPorts,['g',0],)# toggle gyroscope (increases cat speed)
                gyro_status = 0
                print("Gyroscope deactive (disabled)")
        elif int == 1:
            if gyro_status == 0:
                send(goodPorts,['g',0],)# toggle gyroscope (increases cat speed)
                gyro_status = 1
                print("Gyroscope activated (enabled)")
            else:
                print("Gyroscope already active")
        elif int == 2:
            if gyro_status == 0:
                send(goodPorts,['g',0],)# toggle gyroscope (increases cat speed)
                gyro_status = 1
                print("Gyroscope enabled (toggled)")
            else:
                send(goodPorts,['g',0],)# toggle gyroscope (increases cat speed)
                gyro_status = 0
                print("Gyroscope deactivated (toggled)") #Gyro_toggle (toggles gyroscope)
            
def read_inputs():
        command = input() #Reads serial inputs

        if command == "go":
                global speed
                print("\nGo command recognised... let's go!")
                send(goodPorts,['kbalance',1],)  #Stand up and wait for 1 second
                gyro_toggle(1) #Enable gyroscope
                cat_meow(3)                
                print("Set speed from 1-3")
                speed = input()
                print("Speed ", speed, " selected")
                dist_init()
                dist_av()
                motion()  #Start walking forwards and attempt to avoid walls

        elif command == "dist": #prints the distance signal of the ultrasonic sensor
                send(goodPorts,['ksit',0.5],)  #Sit, then look straight ahead and measure the distance to the obstruction
                send(goodPorts,['i', [0, 0, 1, -30], 0.5],)
                print("\nMeasured distance (centimetres)")
                for i in range(20):
                    print(distance()) 
                    time.sleep(1)
                start_cat()

        elif command == "test": #Runs test() once
                print("\nRunning test()")
                test()
                start_cat()

        elif command == "sound": #Runs test() once
                print("\nRunning audio test()")
                audio_test()
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

        elif command == "quit":#Terminate the code
                Nybble_sleep()  #Read inputs and directs to appropriate functions
        
if __name__ == '__main__':
    try:
        '''
        testSchedule is used to test various serial port commands
        '''
        load_sound()
        goodPorts = {}
        connectPort(goodPorts)
        t=threading.Thread(target = keepCheckingPort, args = (goodPorts,))
        t.start()
        parallel = False
        time.sleep(1)
        gyro_toggle(3) # switch gyroscope on (begins off), runs startup code
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

    finally:
        send(goodPorts,['krest',0.5],)
        closeAllSerial(goodPorts)
        os._exit(0) #Main code body
