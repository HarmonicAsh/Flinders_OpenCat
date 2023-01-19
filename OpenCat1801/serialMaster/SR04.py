#Libraries (please install Python GPIO library first!!)
from math import dist
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)     
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
 def direction():
    dist = distance()
    if dist <= 100:
        print("I am too close to something...")
        send(goodPorts,['ksit',1],)  #Sit when an object appears too close
        send(goodPorts,['m', ['0', '0', '1', '10'], 1],) #Look straight ahead
        dist_ahead = dist
        sleep(0.25)
        send(goodPorts,['m', ['0', '-45', '1', '0'], 1],) #Look left
        dist_left = dist
        sleep(0.25)
        send(goodPorts,['m', ['0', '45', '1', '0'], 2],) #Look right
        dist_right = dist
        if dist_left < dist_right:
            send(goodPorts,['kbkL',2],)  #Back up and face the right
            send(goodPorts,['kbalance',10],)  #Stand for a while
        elif dist_left > dist_right:
            send(goodPorts,['kbkR',2],)  #Back up and face the left
             send(goodPorts,['kbalance',10],)  #Stand for a while
        else:
            send(goodPorts,['kbalance',2],)  #Back up
            send(goodPorts,['krest',10],)  #Rest, let's not be defeated by this

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

        
   