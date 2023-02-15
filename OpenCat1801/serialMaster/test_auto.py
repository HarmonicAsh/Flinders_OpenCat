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
        dist = distance()
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

        if dist >= 60:
            motion()


        elif dist_left < dist_right:
            print("Going right..")
            cat_meow(random.randint(0,2))
            right_until()
            #go_left()
        elif dist_left > dist_right:
            print("Going left..")
            cat_meow(random.randint(0,2))
            left_until()
            #go_right()
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

def left_until():
        time_mod = 0.5+1*dist_right/dist_left
        print("Time delay = ", time_mod)
        dist = distance()
        send(goodPorts,['kbkR',time_mod],)
        while dist <= 60:
            time.sleep(0.2)
            dist = distance()
            print("Distance = ", dist, "cm")

        motion() #Left_until (The cat will turn left until the obstruction is nolonger detected)

def right_until():
        time_mod = 0.5+1*dist_left/dist_right
        print("Time delay = ", time_mod)
        dist = distance()
        send(goodPorts,['kbkL',2+2*time_mod],)
        while dist <=60:
            time.sleep(0.2)
            dist = distance()
            print("Distance = ", dist, "cm")
        motion() #Right_until (The cat will turn right until the obstruction is nolonger detected)

def go_right():
        time_mod = dist_right/dist_left
        print("Time factor (face right) = ", time_mod)
        send(goodPorts,['kbkR',2+0.5*speed_mod],)
        
        if speed == "1":
            send(goodPorts,['kcrL',0],)
        elif speed == "2":
            send(goodPorts,['kwkL',0],)
        elif speed == "3":
            send(goodPorts,['ktrL',0],)

        for i in range(round(45*time_mod*speed_mod)):  #Re-orient position and recheck distance throughout progress
            dist = distance()
            if dist <= 18:
                direction()
            else:
                time.sleep(0.05)
                pass #Go_right (The cat will turn right for a given time, based on information (Not implemented))

def go_left():
        time_mod = dist_left/dist_right
        print("Time factor (face left) = ", time_mod)   
        send(goodPorts,['kbkL',2+0.5*speed_mod],)

        if speed == "1":
            send(goodPorts,['kcrR',0],)
        elif speed == "2":
            send(goodPorts,['kwkR',0],)
        elif speed == "3":
            send(goodPorts,['ktrR',0],)
        
        for i in range(round(45*time_mod*speed_mod)):  #Re-orient position and recheck distance throughout progress
            dist = distance()
            if dist <= 18:
                direction()
            else:
                time.sleep(0.05)
                pass #Go_left (The cat will turn left for a given time, based on information (Not implemented))
       
def Nybble_sleep(): #Shuts down Nybble when the script has finished
        print("\nTerminating... farewell!")
        send(goodPorts,['krest',1],)  #Rest
        closeAllSerial(goodPorts)
        logger.info("finish!")
        os._exit(0) #Nybble_sleep (Puts the cat into a shutdown state)

def motion():
        global dist_min
        dist_min = distance()
        global speed_mod
        gyro_toggle(1)

        dist = distance() #Need to add some form of error checking here!
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

        while dist >= 25:
            #dist_av()
            dist = distance()
            print("Distance = ", dist, "cm")
            time.sleep(0.01)
            if dist < dist_min:
                dist_min = dist
            else:
                pass
           
            if dist_min < 50 and gyro_status == 0:
                gyro_toggle(1)
            else:
                pass
        else:
            direction() #Motion (Starts the cat moving forwards, based on speed setting)

        
def dist_av():
        if arr_pos == 5:
            arr_pos = 0
        else:
            pass

        dist_arr[arr_pos] = distance()

        for i in range (5):
            total += dist_arr[i]
        
        dist = total/5
        arr_pos += 1
        print("Distance = ", dist, "cm (internal calc)")
        total = 0
        time.sleep(0.01)
        return dist

def prep_arr():
        dist_arr = [0, 0, 0, 0, 0]
        for i in range(5):
            dist_arr[i] = distance()
            time.sleep(0.1)
            print("Distance ", i, " = ", dist_arr[i])
     
            
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

def dist_av(int):
        global dist_arr
        global arr_pos
             
        if int == 0:
             send(goodPorts,['kbalance',1],)  #Stand up and wait for 1 second
            dist_arr = [0, 0, 0, 0, 0]
            for i in range(5):
                dist_arr[i] = distance()
                time.sleep(0.1)
                print("Distance ", i, " = ", dist_arr[i])
            arr_pos = 0
            total = 0
        
        elif int == 1:
            total = 0
            print("Array full..")
            dist_arr[arr_pos] = distance()
            print("Updated array number")
            for i in range (5):
                total += dist_arr[i]
            print("Total calculated..")
            dist = total/5
            print("Distance = ", dist, "cm (internal calc)")
            time.sleep(0.01)
            arr_pos += 1
            if arr_pos == 5:
                arr_pos = 0
            else:
                pass
        else:
            pass



def test(int):
        dist_av(0)
        while True:
            dist_av(1)
            time.sleep(0.25)

        
        
  

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
     
def init_setup():
        global speed
        global wait_speed
        global arr_pos
        arr_pos = 0
        global has_filled
        global dist_arr
        has_filled = 0
        
        
def read_inputs():
        init_setup()
        command = input() #Reads serial inputs
        if command == "go":
                print("\nGo command recognised... let's go!")
                send(goodPorts,['kbalance',1],)  #Stand up and wait for 1 second
                cat_meow(3)
                print("Set speed from 1-3")
                speed = input()
                
                wait_speed = 1
                while wait_speed == 1:
                    if speed == '1' or speed == '2' or speed == '3':
                        wait_speed=0
                    else:
                        pass
                print("Speed ", speed, " selected")
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
                test(0)
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