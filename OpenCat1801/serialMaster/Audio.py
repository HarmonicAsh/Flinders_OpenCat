#Audio playback module

import time
from pygame import mixer

mixer.init()  #Initialise pigame mixer
cat2 = mixer.Sound("cat2.wav")   #load wav files
mixer.Sound.play(cat2)
time.sleep(1)


def meow(int):
    if int == 0:
        mixer.Sound.play(cat2)
