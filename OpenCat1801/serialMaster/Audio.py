#Audio playback module

import time
from pygame import mixer

mixer.init()  #Initialise pigame mixer
cat1 = mixer.Sound('cat1.mp3')   #load mp3 files
cat2 = mixer.Sound('cat2.mp3') 
cat3 = mixer.Sound('cat3.mp3') 
cat4 = mixer.Sound('cat4.mp3') 


try:
    while True:
        print("Press 1 ~ 4 to play audio")
        command = input()
        print("Playback beginning...")
        if command == "1":
            cat1.play()
            print("Playback finished/n")
        elif command == "2":
            cat2.play()
            print("Playback finished/n")
        elif command == "3":
            cat3.play()
            print("Playback finished/n")
        elif command == "4":
            cat4.play()
            print("Playback finished/n")
