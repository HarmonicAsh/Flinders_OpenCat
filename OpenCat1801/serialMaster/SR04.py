# Test code for the RUS04 built in ultrasonic sensor

#Copied code from SR04.py and modified
#Libraries (please install Python GPIO library first!!)
from math import dist
import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM) #GPIO Mode (BOARD / BCM)
SIG = 18 #set GPIO Pin

def distance():
    GPIO.setup(SIG, GPIO.OUT)
    GPIO.output(SIG, True)
    time.sleep(0.00001)
    GPIO.output(SIG, False)

    StartTime = time.time()
    StopTime = time.time()
    print("Test line 1")
    # save StartTime

    GPIO.setup(SIG, GPIO.IN)
    while GPIO.input(SIG) == 0:
        StartTime = time.time()
    # save time of arrival
    while GPIO.input(SIG) == 1:
        StopTime = time.time()
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


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

        
   