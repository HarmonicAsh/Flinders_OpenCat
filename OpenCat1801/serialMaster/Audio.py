#Audio playback module

import time
from pygame import mixer

mixer.init()  #Initialise pigame mixer
cat1 = mixer.Sound("cat1.wav")   #load wav files
cat2 = mixer.Sound("cat2.wav")   #load wav files
cat3 = mixer.Sound("cat3.wav")   #load wav files
cat4 = mixer.Sound("cat4.wav")   #load wav files

time.sleep(1)


def meow(int):
    if int == 0:
        mixer.Sound.play(cat2)
